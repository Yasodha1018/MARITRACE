import time
import random

def detect_spill(image_bytes):
    """
    Dummy detection – returns synthetic results.
    No numpy/pandas/tensorflow required.
    """
    # Simulate processing delay
    time.sleep(0.5)

    # Generate a random polygon (simple square)
    base_lat = 20.0 + random.uniform(-0.5, 0.5)
    base_lon = 70.0 + random.uniform(-0.5, 0.5)
    polygon = [
        [base_lat, base_lon],
        [base_lat + 0.1, base_lon + 0.1],
        [base_lat + 0.2, base_lon - 0.05],
        [base_lat + 0.05, base_lon - 0.15]
    ]
    area_km2 = random.uniform(5.0, 20.0)
    prob = random.uniform(85, 98)
    severity = "HIGH" if area_km2 > 10 else "MEDIUM" if area_km2 > 5 else "LOW"
    return {
        'spill_probability': round(prob, 1),
        'area_km2': round(area_km2, 2),
        'severity': severity,
        'confidence': round(prob, 1),
        'shape': 'irregular',
        'polygon': polygon,
        'lookalike_classification': {
            'Oil Spill': round(prob, 1),
            'Low Wind': round(random.uniform(1, 5), 1),
            'Natural Slick': round(random.uniform(1, 4), 1),
            'Other': round(random.uniform(0, 2), 1)
        },
        'lat': (polygon[0][0] + polygon[2][0]) / 2,
        'lon': (polygon[0][1] + polygon[2][1]) / 2
    }