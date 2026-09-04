from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VesselTrack(BaseModel):
    mmsi: str
    name: str
    lat: float
    lon: float
    timestamp: datetime
    speed: float
    heading: float