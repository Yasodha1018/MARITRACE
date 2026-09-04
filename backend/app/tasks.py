from celery import Celery
from datetime import datetime, timedelta
import json
from app.core.config import settings
from app.services.satellite_service import SatelliteService
from app.services.ais_service import AISService
from app.services.drift_service import DriftService
from app.services.scoring_service import ScoringEngine
from app.core.database import SessionLocal
from app.models.incident import Incident

celery_app = Celery('maritrace', broker=settings.REDIS_URL)

@celery_app.task
def process_new_satellite_image(image_path: str, metadata: dict):
    """Process a newly acquired satellite image"""
    satellite = SatelliteService()
    
    # Read image
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # Process through ML pipeline
    result = satellite.process_image(image_bytes, metadata)
    
    # Save to database
    db = SessionLocal()
    incident = Incident(
        name=f"Oil Spill detected at {datetime.utcnow().isoformat()}",
        detection_time=datetime.utcnow(),
        location_lat=metadata.get('lat', 0),
        location_lon=metadata.get('lon', 0),
        spill_area_km2=result['area_km2'],
        confidence=result['confidence'],
        severity=result['severity'],
        status='active',
        metadata=result
    )
    db.add(incident)
    db.commit()
    incident_id = incident.id
    db.close()
    
    # Trigger downstream tasks
    run_drift_analysis.delay(incident_id)
    run_vessel_attribution.delay(incident_id)
    
    return incident_id

@celery_app.task
def run_drift_analysis(incident_id: int):
    """Run drift hindcasting and forecasting"""
    db = SessionLocal()
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        return
    
    drift = DriftService()
    result = drift.hindcast(incident.location_lat, incident.location_lon, steps=30)
    
    # Update incident with origin info
    incident.origin_lat = result['origin'][0]
    incident.origin_lon = result['origin'][1]
    incident.origin_confidence = result['origin_confidence']
    db.commit()
    db.close()
    
    return result

@celery_app.task
def run_vessel_attribution(incident_id: int):
    """Run vessel attribution and ranking"""
    db = SessionLocal()
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        return
    
    # Set time window (1 hour before and after detection)
    time_window_start = (incident.detection_time - timedelta(hours=1)).isoformat()
    time_window_end = (incident.detection_time + timedelta(hours=1)).isoformat()
    
    # Get AIS candidates
    ais = AISService()
    candidates = ais.get_candidates(
        incident.origin_lat or incident.location_lat,
        incident.origin_lon or incident.location_lon,
        time_window_start,
        time_window_end
    )
    
    # Score candidates
    scorer = ScoringEngine()
    drift = DriftService().hindcast(incident.location_lat, incident.location_lon)
    
    scored = []
    for v in candidates:
        total, comps, evidence = scorer.compute(
            v, 
            (incident.origin_lat or incident.location_lat, 
             incident.origin_lon or incident.location_lon),
            drift['forward'],
            time_window_start
        )
        scored.append({
            'vessel_id': v['mmsi'],
            'vessel_name': v['name'],
            'total_score': total,
            'components': comps,
            'evidence': evidence
        })
    
    scored.sort(key=lambda x: x['total_score'], reverse=True)
    
    # Store results in incident metadata
    incident.metadata['vessel_candidates'] = scored
    db.commit()
    db.close()
    
    return scored

@celery_app.task
def scheduled_satellite_monitoring():
    """Scheduled task to monitor for new oil spills"""
    # Define areas to monitor (e.g., Indian Ocean regions)
    monitoring_areas = [
        {"name": "Arabian Sea", "bbox": [60, 15, 75, 25]},
        {"name": "Bay of Bengal", "bbox": [80, 10, 95, 20]},
    ]
    
    satellite = SatelliteService()
    for area in monitoring_areas:
        # Search for recent images (last 12 hours)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=12)
        
        images = satellite.search_sentinel1_images(
            area['bbox'],
            start_time.isoformat(),
            end_time.isoformat()
        )
        
        for img in images:
            # Download and process each image
            image_path = satellite.download_image(img['id'])
            process_new_satellite_image.delay(
                image_path,
                {'area': area['name'], 'lat': 20, 'lon': 70}
            )