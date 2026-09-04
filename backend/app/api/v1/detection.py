from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.services.satellite_service import SatelliteService
from app.tasks import process_new_satellite_image
import tempfile
import os

router = APIRouter()

@router.post("/detect")
async def detect_spill(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Detect oil spill from uploaded satellite image"""
    image_bytes = await file.read()
    satellite = SatelliteService()
    result = satellite.process_image(image_bytes, {"filename": file.filename})
    
    # Trigger background processing for AIS correlation
    if background_tasks and result.get('spill_probability', 0) > 50:
        # Save image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tiff') as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name
        
        # Start background task
        background_tasks.add_task(
            process_new_satellite_image,
            tmp_path,
            {'lat': 20, 'lon': 70, 'filename': file.filename}
        )
    
    return result

@router.post("/detect/url")
async def detect_from_url(image_url: str, background_tasks: BackgroundTasks = None):
    """Detect oil spill from satellite image URL"""
    import requests
    response = requests.get(image_url)
    image_bytes = response.content
    
    satellite = SatelliteService()
    result = satellite.process_image(image_bytes, {"url": image_url})
    
    if background_tasks and result.get('spill_probability', 0) > 50:
        background_tasks.add_task(
            process_new_satellite_image,
            None,  # Will download from URL in task
            {'url': image_url, 'lat': 20, 'lon': 70}
        )
    
    return result

@router.get("/images/search")
async def search_satellite_images(bbox: str, start_date: str, end_date: str):
    """Search for Sentinel-1 images in a given area"""
    bbox_list = [float(x) for x in bbox.split(',')]
    satellite = SatelliteService()
    images = satellite.search_sentinel1_images(bbox_list, start_date, end_date)
    return {"images": images}