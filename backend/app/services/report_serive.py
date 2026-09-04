from datetime import datetime

class ReportService:
    def generate(self, incident, candidates):
        report = {
            "incident_id": incident.id,
            "detection_time": incident.detection_time.isoformat(),
            "location": f"{incident.location_lat}, {incident.location_lon}",
            "spill_area": incident.spill_area_km2,
            "confidence": incident.confidence,
            "severity": incident.severity,
            "origin": f"{incident.origin_lat}, {incident.origin_lon}",
            "origin_confidence": incident.origin_confidence,
            "candidates": [
                {
                    "vessel": c.vessel_name,
                    "score": c.total_score,
                    "evidence": c.evidence
                } for c in candidates
            ]
        }
        return report