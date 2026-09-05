from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Incident, SpillPolygon
from detection import detect_spill
from drift import hindcast
from ais import get_candidates
from scoring import ScoringEngine
from report import generate_report
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maritrace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)  # allow frontend

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    image_bytes = file.read()
    result = detect_spill(image_bytes)
    # Save incident to DB
    incident = Incident(
        name=f"Spill_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        lat=result['lat'],
        lon=result['lon'],
        area_km2=result['area_km2'],
        confidence=result['confidence'],
        severity=result['severity'],
        spill_metadata=result          # <-- FIXED: renamed from 'metadata'
    )
    db.session.add(incident)
    db.session.commit()
    # Save polygon
    if result.get('polygon'):
        poly = SpillPolygon(
            incident_id=incident.id,
            geometry=json.dumps(result['polygon']),
            area=result['area_km2'],
            confidence=result['confidence']
        )
        db.session.add(poly)
        db.session.commit()
    return jsonify({
        'incident_id': incident.id,
        **result
    })

@app.route('/api/drift', methods=['POST'])
def drift():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    steps = data.get('steps', 20)
    if lat is None or lon is None:
        return jsonify({'error': 'Missing lat/lon'}), 400
    result = hindcast(lat, lon, steps)
    return jsonify(result)

@app.route('/api/candidates', methods=['POST'])
def candidates():
    data = request.json
    origin_lat = data.get('origin_lat')
    origin_lon = data.get('origin_lon')
    time_start = data.get('time_start')
    time_end = data.get('time_end')
    if None in (origin_lat, origin_lon, time_start, time_end):
        return jsonify({'error': 'Missing parameters'}), 400
    candidates = get_candidates(origin_lat, origin_lon, time_start, time_end)
    return jsonify({'candidates': candidates})

@app.route('/api/rank', methods=['POST'])
def rank():
    data = request.json
    origin_lat = data.get('origin_lat')
    origin_lon = data.get('origin_lon')
    time_start = data.get('time_start')
    time_end = data.get('time_end')
    incident_id = data.get('incident_id')
    if None in (origin_lat, origin_lon, time_start, time_end, incident_id):
        return jsonify({'error': 'Missing parameters'}), 400
    # Get candidates
    candidates = get_candidates(origin_lat, origin_lon, time_start, time_end)
    # Get drift trajectory
    drift = hindcast(origin_lat, origin_lon)
    scorer = ScoringEngine()
    scored = []
    for v in candidates:
        total, comps, evidence = scorer.compute(v, (origin_lat, origin_lon), drift['forward'], time_start)
        scored.append({
            'vessel_id': v['mmsi'],
            'vessel_name': v['name'],
            'total_score': total,
            'components': comps,
            'evidence': evidence
        })
    scored.sort(key=lambda x: x['total_score'], reverse=True)
    return jsonify({'candidates': scored})

@app.route('/api/report', methods=['POST'])
def report():
    data = request.json
    incident_id = data.get('incident_id')
    if not incident_id:
        return jsonify({'error': 'Missing incident_id'}), 400
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({'error': 'Incident not found'}), 404
    # For demo, get dummy candidates (or from DB)
    dummy_candidates = [
        {'name': 'Vessel A', 'score': 91, 'evidence': ['Proximity', 'Temporal match']},
        {'name': 'Vessel B', 'score': 68, 'evidence': ['Proximity']}
    ]
    report_data = generate_report(incident, dummy_candidates)
    return jsonify(report_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)