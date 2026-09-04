from pydantic import BaseModel
from typing import Optional, List

class DetectionResult(BaseModel):
    spill_probability: float
    area_km2: float
    severity: str
    confidence: float
    shape: str
    polygon: Optional[List[List[float]]] = None
    lookalike_classification: dict  # e.g., {"oil": 94, "low_wind": 3, ...}