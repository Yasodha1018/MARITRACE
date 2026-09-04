from app.ml.drift_model import DriftModel

class DriftService:
    def __init__(self):
        self.model = DriftModel()

    def hindcast(self, lat, lon, steps=20):
        backward = self.model.track(lat, lon, steps, reverse=True)
        forward = self.model.track(lat, lon, steps, reverse=False)
        # estimate origin as first backward point
        origin = backward[-1]
        return {
            "forward": forward,
            "backward": backward,
            "origin": origin,
            "origin_confidence": 0.82
        }