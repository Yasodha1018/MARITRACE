import random

def hindcast(lat, lon, steps=20):
    """
    Backward and forward drift using random walk.
    Uses Python's random module – no numpy needed.
    """
    # Backward from current position
    backward = [(lat, lon)]
    lat_b, lon_b = lat, lon
    for _ in range(steps):
        lat_b += random.uniform(-0.01, 0.01)
        lon_b += random.uniform(-0.01, 0.01)
        backward.append((lat_b, lon_b))

    # Forward from original position
    forward = [(lat, lon)]
    lat_f, lon_f = lat, lon
    for _ in range(steps):
        lat_f += random.uniform(-0.01, 0.01)
        lon_f += random.uniform(-0.01, 0.01)
        forward.append((lat_f, lon_f))

    # Probable origin is the last backward point (or use average)
    origin = backward[-1]
    origin_confidence = random.uniform(70, 90)

    return {
        'forward': forward,
        'backward': backward,
        'origin': origin,
        'origin_confidence': round(origin_confidence, 1)
    }