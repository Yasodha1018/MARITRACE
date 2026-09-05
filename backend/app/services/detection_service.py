from app.ml.oil_spill_model import OilSpillDetector
from PIL import Image
import io
import numpy as np

class DetectionService:
    def __init__(self):
        self.detector = OilSpillDetector()

    def process(self, image_bytes):
        # Load image to get original dimensions
        img = Image.open(io.BytesIO(image_bytes))
        original_shape = img.size  # (width, height)

        # Run model
        mask, confidence_map = self.detector.predict_mask(image_bytes)

        # Extract polygon
        polygon = self.detector.extract_polygon(mask, original_shape)

        # Estimate area
        area_km2 = self.detector.estimate_area(mask)

        # Compute confidence (average of oil class probability where mask > 0)
        if np.any(mask > 0):
            prob = float(np.mean(confidence_map[mask > 0]) * 100)
        else:
            prob = 0.0

        severity = "HIGH" if area_km2 > 10 else "MEDIUM" if area_km2 > 2 else "LOW"

        return {
            "spill_probability": prob,
            "area_km2": area_km2,
            "severity": severity,
            "confidence": prob,
            "shape": "irregular" if polygon else "none",
            "polygon": polygon,
            "lookalike_classification": {
                "oil": round(prob, 1),
                "low_wind": round((100 - prob) * 0.5, 1),
                "natural_slick": round((100 - prob) * 0.3, 1),
                "other": round((100 - prob) * 0.2, 1)
            }
        }