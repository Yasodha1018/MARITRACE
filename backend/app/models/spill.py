from sqlalchemy import Column, Integer, Float, ForeignKey
from geoalchemy2 import Geometry
from app.models.incident import Base

class Spill(Base):
    __tablename__ = "spills"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    geometry = Column(Geometry('POLYGON', srid=4326))
    area = Column(Float)
    confidence = Column(Float)