import csv
import os
from geopy.distance import distance
from datetime import datetime

def load_ais_data(filepath='./data/ais/sample_ais.csv'):
    """Load AIS data from CSV using built-in csv module."""
    if not os.path.exists(filepath):
        # Create dummy data if file missing
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['mmsi', 'name', 'lat', 'lon', 'timestamp', 'speed', 'heading'])
            writer.writerow(['123456789', 'Tanker Alpha', '20.5', '70.2', '2025-09-04T08:30:00Z', '5.2', '120'])
            writer.writerow(['987654321', 'Cargo Bravo', '20.3', '70.0', '2025-09-04T09:00:00Z', '8.1', '90'])
        return load_ais_data(filepath)  # reload after creation
    
    rows = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert types
            row['lat'] = float(row['lat'])
            row['lon'] = float(row['lon'])
            row['speed'] = float(row['speed'])
            row['heading'] = float(row['heading'])
            rows.append(row)
    return rows

def get_candidates(origin_lat, origin_lon, time_start, time_end, radius_km=20):
    data = load_ais_data()
    time_start = datetime.fromisoformat(time_start.replace('Z', '+00:00'))
    time_end = datetime.fromisoformat(time_end.replace('Z', '+00:00'))
    
    candidates = []
    # Group by mmsi
    vessels = {}
    for row in data:
        mmsi = row['mmsi']
        if mmsi not in vessels:
            vessels[mmsi] = []
        vessels[mmsi].append(row)
    
    for mmsi, rows in vessels.items():
        # Filter by time
        filtered = []
        for r in rows:
            ts = datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00'))
            if time_start <= ts <= time_end:
                filtered.append(r)
        if not filtered:
            continue
        
        # Compute average distance to origin
        distances = []
        for r in filtered:
            dist = distance((origin_lat, origin_lon), (r['lat'], r['lon'])).km
            distances.append(dist)
        avg_dist = sum(distances) / len(distances)
        if avg_dist > radius_km:
            continue
        
        candidates.append({
            'mmsi': mmsi,
            'name': filtered[0]['name'],
            'track': filtered,
            'avg_distance': avg_dist
        })
    return candidates