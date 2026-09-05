from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/rank")
def rank_vessels(incident_id: int = Body(...), origin_lat: float = Body(...),
                 origin_lon: float = Body(...), time_start: str = Body(...),
                 time_end: str = Body(...)):
    return {
        "candidates": [
            {
                "vessel_id": "123456789",
                "vessel_name": "Tanker Alpha",
                "total_score": 91,
                "components": {"proximity": 85, "temporal": 80, "trajectory": 75, "drift_consistency": 70, "ais_behavior": 65},
                "evidence": ["Close to origin", "Present during spill window", "Trajectory intersects origin"]
            },
            {
                "vessel_id": "987654321",
                "vessel_name": "Cargo Bravo",
                "total_score": 68,
                "components": {"proximity": 60, "temporal": 70, "trajectory": 55, "drift_consistency": 50, "ais_behavior": 45},
                "evidence": ["Moderate distance", "Time match weak"]
            }
        ]
    }