from fastapi import APIRouter, Body
from app.services.ais_service import AISService

router = APIRouter()

@router.post("/candidates")
def get_candidates(origin_lat: float = Body(...), origin_lon: float = Body(...),
                   time_start: str = Body(...), time_end: str = Body(...)):
    ais = AISService()
    candidates = ais.get_candidates(origin_lat, origin_lon, time_start, time_end)
    return {"candidates": candidates}