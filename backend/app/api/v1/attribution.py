from fastapi import APIRouter, Body
from app.services.scoring_service import ScoringEngine
from app.services.ais_service import AISService
from app.services.drift_service import DriftService
from app.schemas.attribution import AttributionResult, VesselScore

router = APIRouter()

@router.post("/rank")
def rank_vessels(incident_id: int, origin_lat: float = Body(...), origin_lon: float = Body(...),
                 time_start: str = Body(...), time_end: str = Body(...)):
    # Get candidates from AIS
    ais = AISService()
    candidates = ais.get_candidates(origin_lat, origin_lon, time_start, time_end)
    # Get drift trajectory
    ds = DriftService()
    drift = ds.hindcast(origin_lat, origin_lon)
    # Score each candidate
    scorer = ScoringEngine()
    scored = []
    for v in candidates:
        total, comps, evidence = scorer.compute(v, (origin_lat, origin_lon), drift['forward'], time_start)
        scored.append(VesselScore(
            vessel_id=v['mmsi'],
            vessel_name=v['name'],
            total_score=total,
            components=comps,
            evidence=evidence
        ))
    scored.sort(key=lambda x: x.total_score, reverse=True)
    return AttributionResult(candidates=scored)