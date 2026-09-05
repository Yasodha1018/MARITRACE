from datetime import datetime

def generate_report(incident, candidates):
    report = {
        'incident_id': incident.id,
        'detection_time': incident.detection_time.isoformat(),
        'location': f"{incident.lat}, {incident.lon}",
        'spill_area': incident.area_km2,
        'confidence': incident.confidence,
        'severity': incident.severity,
        'origin': f"{incident.origin_lat}, {incident.origin_lon}",
        'origin_confidence': incident.origin_confidence,
        'candidates': [
            {
                'vessel': c['name'],
                'score': round(c.get('score', 0), 2),
                'evidence': c.get('evidence', [])
            }
            for c in candidates
        ]
    }
    return report