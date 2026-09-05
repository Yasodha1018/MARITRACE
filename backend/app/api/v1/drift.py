from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/hindcast")
def hindcast(lat: float = Body(...), lon: float = Body(...), steps: int = 20):
    forward = [(lat + i * 0.01, lon + i * 0.01) for i in range(steps)]
    backward = [(lat - i * 0.01, lon - i * 0.01) for i in range(steps)]
    return {
        "forward": forward,
        "backward": backward,
        "origin": (lat - 0.2, lon - 0.2),
        "origin_confidence": 82.0
    }