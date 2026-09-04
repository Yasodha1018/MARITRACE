class ScoringEngine:
    WEIGHTS = {
        "proximity": 0.30,
        "temporal": 0.25,
        "trajectory": 0.25,
        "drift_consistency": 0.10,
        "ais_behavior": 0.10
    }

    def compute(self, vessel_data, origin, drift_trajectory, spill_time):
        scores = {}
        scores["proximity"] = self._proximity_score(vessel_data, origin)
        scores["temporal"] = self._temporal_score(vessel_data, spill_time)
        scores["trajectory"] = self._trajectory_score(vessel_data, origin)
        scores["drift_consistency"] = self._drift_consistency(vessel_data, drift_trajectory)
        scores["ais_behavior"] = self._behavior_score(vessel_data)
        total = sum(scores[k] * self.WEIGHTS[k] for k in scores)
        # Build evidence list
        evidence = []
        if scores["proximity"] > 70:
            evidence.append("Vessel was close to origin")
        if scores["temporal"] > 70:
            evidence.append("Present during estimated spill window")
        if scores["trajectory"] > 70:
            evidence.append("Trajectory intersects origin region")
        if scores["drift_consistency"] > 70:
            evidence.append("Direction compatible with drift")
        if scores["ais_behavior"] > 70:
            evidence.append("AIS transmission anomaly detected")
        return total, scores, evidence

    # Dummy scoring functions (replace with real logic)
    def _proximity_score(self, v, origin): return 85
    def _temporal_score(self, v, t): return 80
    def _trajectory_score(self, v, origin): return 75
    def _drift_consistency(self, v, drift): return 70
    def _behavior_score(self, v): return 65