from fastapi import APIRouter, Body
from app.services.drift_service import DriftService

router = APIRouter()

@router.post("/hindcast")
def hindcast(lat: float = Body(...), lon: float = Body(...), steps: int = 20):
    ds = DriftService()
    result = ds.hindcast(lat, lon, steps)
    return result