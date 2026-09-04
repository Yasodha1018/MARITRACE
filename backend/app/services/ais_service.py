import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from geopy.distance import distance
from typing import List, Dict, Optional
import os

class AISService:
    def __init__(self, data_path: str = "./data/ais/"):
        self.data_path = data_path
        os.makedirs(data_path, exist_ok=True)
        
    def fetch_ais_from_marinecadastre(self, 
                                       bbox: List[float], 
                                       start_date: str, 
                                       end_date: str,
                                       vessel_type: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch AIS data from MarineCadastre.gov AccessAIS system.
        
        bbox: [min_lon, min_lat, max_lon, max_lat]
        start_date/end_date: ISO format dates
        
        MarineCadastre.gov provides AIS data through their AccessAIS application:
        https://marinecadastre.gov/ais/[reference:9]
        """
        # Build query parameters
        params = {
            "format": "csv",
            "geometry": f"POLYGON(({bbox[0]} {bbox[1]}, {bbox[2]} {bbox[1]}, {bbox[2]} {bbox[3]}, {bbox[0]} {bbox[3]}, {bbox[0]} {bbox[1]}))",
            "time_start": start_date,
            "time_end": end_date
        }
        
        # Note: MarineCadastre requires custom data orders via their map interface[reference:10]
        # For automated access, use their API or download pre-processed data
        
        # For demo, return sample AIS data
        return self._get_sample_ais_data()
    
    def _get_sample_ais_data(self):
        """Generate sample AIS data for demonstration"""
        # Create sample vessel tracks
        vessels = [
            {"mmsi": "123456789", "name": "Tanker Alpha", "lat": 20.5, "lon": 70.2, 
             "timestamp": "2025-09-04T08:30:00Z", "speed": 5.2, "heading": 120, "type": "Tanker"},
            {"mmsi": "987654321", "name": "Cargo Bravo", "lat": 20.8, "lon": 70.5, 
             "timestamp": "2025-09-04T08:45:00Z", "speed": 8.7, "heading": 90, "type": "Cargo"},
            {"mmsi": "456789123", "name": "Fishing Charlie", "lat": 19.5, "lon": 69.8, 
             "timestamp": "2025-09-04T08:15:00Z", "speed": 2.3, "heading": 45, "type": "Fishing"},
            {"mmsi": "789123456", "name": "Container Delta", "lat": 21.2, "lon": 71.0, 
             "timestamp": "2025-09-04T09:00:00Z", "speed": 12.1, "heading": 180, "type": "Container"},
            {"mmsi": "321654987", "name": "Tanker Echo", "lat": 20.3, "lon": 70.1, 
             "timestamp": "2025-09-04T08:20:00Z", "speed": 4.5, "heading": 60, "type": "Tanker"}
        ]
        
        # Create track points for each vessel
        tracks = []
        for v in vessels:
            # Generate 10 track points
            for i in range(10):
                dt = datetime.fromisoformat(v["timestamp"].replace('Z', '+00:00'))
                track_time = dt + timedelta(minutes=i*5)
                tracks.append({
                    "mmsi": v["mmsi"],
                    "name": v["name"],
                    "lat": v["lat"] + i * 0.01,
                    "lon": v["lon"] + i * 0.01,
                    "timestamp": track_time.isoformat().replace('+00:00', 'Z'),
                    "speed": v["speed"] + i * 0.1,
                    "heading": v["heading"] + i * 2,
                    "vessel_type": v["type"]
                })
        
        return pd.DataFrame(tracks)
    
    def get_candidates(self, origin_lat: float, origin_lon: float, 
                      time_window_start: str, time_window_end: str,
                      radius_km: float = 20) -> List[Dict]:
        """Get vessel candidates near the spill origin"""
        # Fetch AIS data (or use sample)
        df = self.fetch_ais_from_marinecadastre(
            [origin_lon - 1, origin_lat - 1, origin_lon + 1, origin_lat + 1],
            time_window_start,
            time_window_end
        )
        
        # Filter by time
        start = datetime.fromisoformat(time_window_start.replace('Z', '+00:00'))
        end = datetime.fromisoformat(time_window_end.replace('Z', '+00:00'))
        df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
        df = df[(df['timestamp_dt'] >= start) & (df['timestamp_dt'] <= end)]
        
        # Calculate distance to origin
        def calc_distance(row):
            return distance((origin_lat, origin_lon), (row['lat'], row['lon'])).km
        
        df['distance'] = df.apply(calc_distance, axis=1)
        df = df[df['distance'] <= radius_km]
        
        # Group by vessel
        candidates = []
        for mmsi, group in df.groupby('mmsi'):
            candidates.append({
                'mmsi': mmsi,
                'name': group.iloc[0]['name'],
                'vessel_type': group.iloc[0]['vessel_type'],
                'track': group[['lat','lon','timestamp','speed','heading']].to_dict('records'),
                'avg_distance': group['distance'].mean(),
                'min_distance': group['distance'].min(),
                'time_span': (group['timestamp_dt'].max() - group['timestamp_dt'].min()).total_seconds() / 3600
            })
        
        return candidates