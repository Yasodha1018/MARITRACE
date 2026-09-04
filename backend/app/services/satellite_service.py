import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET
from app.ml.oil_spill_model import OilSpillDetector

class SatelliteService:
    def __init__(self):
        self.detector = OilSpillDetector()
        self.api_base = "https://scihub.copernicus.eu/dhus"
        # Add your Copernicus Open Access Hub credentials
        self.username = os.getenv("COPERNICUS_USERNAME", "")
        self.password = os.getenv("COPERNICUS_PASSWORD", "")
    
    def search_sentinel1_images(self, 
                                bbox: List[float], 
                                start_date: str, 
                                end_date: str,
                                max_results: int = 10) -> List[Dict]:
        """
        Search for Sentinel-1 SAR images in a given area and time range.
        bbox: [min_lon, min_lat, max_lon, max_lat]
        """
        # Construct query
        query = f"""
        <entry>
            <title>Sentinel-1</title>
            <category term="product" />
            <link rel="search" href="?q=*" />
            <id>urn:ogc:def:query:OGC-CSW::1.1.0:AnyText</id>
            <query type="csw:Query">
                <csw:Constraint version="1.1.0">
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsEqualTo>
                                <ogc:PropertyName>platformname</ogc:PropertyName>
                                <ogc:Literal>Sentinel-1</ogc:Literal>
                            </ogc:PropertyIsEqualTo>
                            <ogc:PropertyIsEqualTo>
                                <ogc:PropertyName>producttype</ogc:PropertyName>
                                <ogc:Literal>SLC</ogc:Literal>
                            </ogc:PropertyIsEqualTo>
                            <ogc:PropertyIsWithin>
                                <ogc:PropertyName>Oscar:footprint</ogc:PropertyName>
                                <gml:Polygon>
                                    <gml:exterior>
                                        <gml:LinearRing>
                                            <gml:posList>
                                                {bbox[1]} {bbox[0]} 
                                                {bbox[3]} {bbox[0]} 
                                                {bbox[3]} {bbox[2]} 
                                                {bbox[1]} {bbox[2]} 
                                                {bbox[1]} {bbox[0]}
                                            </gml:posList>
                                        </gml:LinearRing>
                                    </gml:exterior>
                                </gml:Polygon>
                            </ogc:PropertyIsWithin>
                            <ogc:PropertyIsBetween>
                                <ogc:PropertyName>beginposition</ogc:PropertyName>
                                <ogc:LowerBoundary>{start_date}</ogc:LowerBoundary>
                                <ogc:UpperBoundary>{end_date}</ogc:UpperBoundary>
                            </ogc:PropertyIsBetween>
                        </ogc:And>
                    </ogc:Filter>
                </csw:Constraint>
            </query>
        </entry>
        """
        
        # Make request to Copernicus Open Access Hub
        # For demo, return sample data
        return self._get_sample_images()
    
    def _get_sample_images(self):
        """Return sample images for demo purposes"""
        return [
            {
                "id": "S1A_IW_SLC__1SDV_20250904T083012_20250904T083039_045678_056789_1234",
                "title": "Sentinel-1A IW SLC",
                "date": "2025-09-04T08:30:12Z",
                "url": "https://scihub.copernicus.eu/dhus/odata/v1/Products('S1A_IW_SLC__1SDV_20250904T083012_20250904T083039_045678_056789_1234')/$value",
                "footprint": {
                    "type": "Polygon",
                    "coordinates": [[[70, 20], [71, 20], [71, 21], [70, 21], [70, 20]]]
                }
            }
        ]
    
    def download_image(self, product_id: str, output_dir: str = "./data/satellite/"):
        """Download satellite image product"""
        os.makedirs(output_dir, exist_ok=True)
        # Implementation for downloading from Copernicus
        # For demo, return a sample image path
        return os.path.join(output_dir, f"{product_id}.tiff")
    
    def process_image(self, image_bytes, metadata: Dict = None):
        """Process a satellite image through the ML pipeline"""
        # Detect oil spill
        mask, confidence_map = self.detector.predict_mask(image_bytes)
        
        # Get original image dimensions
        from PIL import Image
        img = Image.open(io.BytesIO(image_bytes))
        original_shape = img.size
        
        # Extract polygon
        polygon = self.detector.extract_polygon(mask, original_shape)
        
        # Estimate area
        area_km2 = self.detector.estimate_area(mask)
        
        # Calculate confidence
        avg_confidence = float(np.mean(confidence_map[mask > 0])) if np.any(mask > 0) else 0
        
        # Classify severity
        severity, description = self.detector.classify_severity(area_km2, avg_confidence * 100)
        
        return {
            "spill_probability": avg_confidence * 100,
            "area_km2": area_km2,
            "severity": severity,
            "severity_description": description,
            "confidence": avg_confidence * 100,
            "shape": "irregular",
            "polygon": polygon,
            "mask": mask.tolist(),
            "lookalike_classification": self._classify_lookalikes(confidence_map),
            "metadata": metadata or {}
        }
    
    def _classify_lookalikes(self, confidence_map):
        """Classify dark regions as oil or look-alikes"""
        # Simple heuristic - in production use a separate classifier
        high_conf = np.sum(confidence_map > 0.8)
        med_conf = np.sum((confidence_map > 0.5) & (confidence_map <= 0.8))
        low_conf = np.sum(confidence_map <= 0.5)
        total = high_conf + med_conf + low_conf
        
        return {
            "oil_spill": round((high_conf / max(total, 1)) * 100, 1),
            "low_wind_zone": round((med_conf / max(total, 1)) * 30, 1),
            "natural_slick": round((low_conf / max(total, 1)) * 20, 1),
            "other": round(100 - (high_conf / max(total, 1) * 100 + 
                                  med_conf / max(total, 1) * 30 + 
                                  low_conf / max(total, 1) * 20), 1)
        }