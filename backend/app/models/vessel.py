from sqlalchemy import Column, Integer, String, Float, DateTime
from app.models.incident import Base

class Vessel(Base):
    __tablename__ = "vessels"
    id = Column(Integer, primary_key=True, index=True)
    mmsi = Column(String, unique=True, index=True)
    name = Column(String)
    vessel_type = Column(String)
    # additional fields