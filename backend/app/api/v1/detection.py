from fastapi import APIRouter, UploadFile, File
import random

router = APIRouter()

@router.post("/detect")
async def detect_spill(file: UploadFile = File(...)):
    # Return dummy detection result
    return {
        "spill_probability": round(random.uniform(70, 99), 1),
        "area_km2": round(random.uniform(1, 25), 2),
        "severity": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "confidence": round(random.uniform(80, 98), 1),
        "shape": "irregular",
        "polygon": [[100, 100], [200, 150], [180, 300], [80, 250]],
        "lookalike_classification": {
            "oil": 94,
            "low_wind": 3,
            "natural_slick": 2,
            "other": 1
        }
    }