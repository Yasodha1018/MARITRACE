from fastapi import APIRouter, UploadFile, File
from app.services.detection_service import DetectionService

router = APIRouter()

@router.post("/detect")
async def detect_spill(file: UploadFile = File(...)):
    image_bytes = await file.read()
    detector = DetectionService()
    result = detector.process(image_bytes)
    return result