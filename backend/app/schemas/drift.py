from pydantic import BaseModel
from typing import List, Tuple

class DriftTrajectory(BaseModel):
    forward: List[Tuple[float, float]]  # list of (lat, lon)
    backward: List[Tuple[float, float]]
    origin: Tuple[float, float]
    origin_confidence: float