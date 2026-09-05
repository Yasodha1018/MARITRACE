from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    detection_time = db.Column(db.DateTime, default=datetime.utcnow)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    area_km2 = db.Column(db.Float)
    confidence = db.Column(db.Float)
    severity = db.Column(db.String(20))   # LOW, MEDIUM, HIGH
    origin_lat = db.Column(db.Float, nullable=True)
    origin_lon = db.Column(db.Float, nullable=True)
    origin_confidence = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='active')
    spill_metadata = db.Column(db.JSON, nullable=True)   # <-- renamed

class Vessel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mmsi = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100))
    vessel_type = db.Column(db.String(50))

class SpillPolygon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))
    geometry = db.Column(db.String)  # store GeoJSON as string for simplicity
    area = db.Column(db.Float)
    confidence = db.Column(db.Float)