from pydantic import BaseModel
from typing import Dict, List

class VesselScore(BaseModel):
    vessel_id: str
    vessel_name: str
    total_score: float
    components: Dict[str, float]  # proximity, temporal, trajectory, etc.
    evidence: List[str]

class AttributionResult(BaseModel):
    candidates: List[VesselScore]