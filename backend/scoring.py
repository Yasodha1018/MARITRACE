class ScoringEngine:
    WEIGHTS = {
        'proximity': 0.30,
        'temporal': 0.25,
        'trajectory': 0.25,
        'drift_consistency': 0.10,
        'ais_behavior': 0.10
    }

    def compute(self, vessel_data, origin, drift_trajectory, spill_time):
        # Dummy scores – replace with real logic
        scores = {
            'proximity': 85,
            'temporal': 80,
            'trajectory': 75,
            'drift_consistency': 70,
            'ais_behavior': 65
        }
        total = sum(scores[k] * self.WEIGHTS[k] for k in scores)
        evidence = []
        if scores['proximity'] > 70:
            evidence.append('Vessel was close to origin')
        if scores['temporal'] > 70:
            evidence.append('Present during estimated spill window')
        if scores['trajectory'] > 70:
            evidence.append('Trajectory intersects origin region')
        if scores['drift_consistency'] > 70:
            evidence.append('Direction compatible with drift')
        if scores['ais_behavior'] > 70:
            evidence.append('AIS transmission anomaly detected')
        return total, scores, evidence