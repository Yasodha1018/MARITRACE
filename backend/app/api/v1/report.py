from fastapi import APIRouter, Body
from datetime import datetime

router = APIRouter()

@router.post("/generate")
def generate_report(incident_id: int = Body(...)):
    return {
        "incident_id": incident_id,
        "detection_time": datetime.utcnow().isoformat(),
        "location": "20.0, 70.0",
        "spill_area": 14.7,
        "confidence": 94.0,
        "severity": "HIGH",
        "origin": "19.8, 69.8",
        "origin_confidence": 82.0,
        "candidates": [
            {"vessel": "Tanker Alpha", "score": 91, "evidence": ["Close", "Timing match"]},
            {"vessel": "Cargo Bravo", "score": 68, "evidence": ["Moderate"]}
        ]
    }