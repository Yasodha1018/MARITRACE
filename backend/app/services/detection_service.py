from app.ml.oil_spill_model import OilSpillDetector
from app.core.config import settings
import numpy as np
from PIL import Image
import io

class DetectionService:
    def __init__(self):
        self.detector = OilSpillDetector(settings.MODEL_PATH)

    def process(self, image_bytes):
        # Get original image shape
        img = Image.open(io.BytesIO(image_bytes))
        original_shape = img.size  # (width, height)
        mask = self.detector.predict_mask(image_bytes)
        polygon = self.detector.extract_polygon(mask, original_shape)
        # Compute area in km² (simplified: assume pixel resolution known)
        area_km2 = np.sum(mask > 0) * 0.01  # dummy scale
        prob = 0.94  # dummy
        severity = "HIGH" if area_km2 > 10 else "MEDIUM" if area_km2 > 2 else "LOW"
        return {
            "spill_probability": prob,
            "area_km2": area_km2,
            "severity": severity,
            "confidence": prob,
            "shape": "irregular",
            "polygon": polygon,
            "lookalike_classification": {"oil": 94, "low_wind": 3, "natural_slick": 2, "other": 1}
        }