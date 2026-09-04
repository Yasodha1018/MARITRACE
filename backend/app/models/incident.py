from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from geoalchemy2 import Geometry

Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    detection_time = Column(DateTime, default=datetime.utcnow)
    location_lat = Column(Float)
    location_lon = Column(Float)
    spill_area_km2 = Column(Float)
    confidence = Column(Float)
    severity = Column(String)  # LOW, MEDIUM, HIGH
    origin_lat = Column(Float, nullable=True)
    origin_lon = Column(Float, nullable=True)
    origin_confidence = Column(Float, nullable=True)
    predicted_affected_area = Column(Float, nullable=True)
    status = Column(String, default="active")
    metadata = Column(JSON)