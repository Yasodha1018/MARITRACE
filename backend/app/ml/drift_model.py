import numpy as np

class DriftModel:
    def __init__(self, current_data=None, wind_data=None):
        # In real implementation, load gridded data
        self.current_data = current_data
        self.wind_data = wind_data

    def track(self, start_lat, start_lon, steps, dt=3600, reverse=False):
        # Simple random walk demo
        trajectory = [(start_lat, start_lon)]
        lat, lon = start_lat, start_lon
        for _ in range(steps):
            # simulate drift (replace with real physics)
            lat += np.random.normal(0, 0.01) * (1 if reverse else -1)
            lon += np.random.normal(0, 0.01) * (1 if reverse else -1)
            trajectory.append((lat, lon))
        return trajectory