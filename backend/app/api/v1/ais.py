from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/candidates")
def get_candidates(origin_lat: float = Body(...), origin_lon: float = Body(...),
                   time_start: str = Body(...), time_end: str = Body(...)):
    return {
        "candidates": [
            {
                "mmsi": "123456789",
                "name": "Tanker Alpha",
                "vessel_type": "Tanker",
                "track": [{"lat": 20.5, "lon": 70.2, "timestamp": time_start, "speed": 5.2, "heading": 120}],
                "avg_distance": 3.2,
                "min_distance": 2.1,
                "time_span": 1.5
            },
            {
                "mmsi": "987654321",
                "name": "Cargo Bravo",
                "vessel_type": "Cargo",
                "track": [{"lat": 21.0, "lon": 70.5, "timestamp": time_end, "speed": 8.7, "heading": 90}],
                "avg_distance": 8.5,
                "min_distance": 7.8,
                "time_span": 2.0
            }
        ]
    }