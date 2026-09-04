from fastapi import APIRouter, Body
from app.services.report_service import ReportService
from app.models.incident import Incident
from app.core.database import SessionLocal

router = APIRouter()

@router.post("/generate")
def generate_report(incident_id: int = Body(...)):
    db = SessionLocal()
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # For demo, we create dummy candidates
    candidates = []  # would come from scoring
    report = ReportService().generate(incident, candidates)
    return report