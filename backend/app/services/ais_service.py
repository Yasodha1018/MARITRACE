import pandas as pd
from datetime import datetime, timedelta
from geopy.distance import distance

class AISService:
    def __init__(self, data_path="./data/ais/sample_ais.csv"):
        self.df = pd.read_csv(data_path)

    def get_candidates(self, origin_lat, origin_lon, time_window_start, time_window_end, radius_km=20):
        # Filter by time
        mask = (self.df['timestamp'] >= time_window_start) & (self.df['timestamp'] <= time_window_end)
        df_filtered = self.df[mask].copy()
        # Filter by distance to origin
        df_filtered['distance'] = df_filtered.apply(
            lambda row: distance((origin_lat, origin_lon), (row['lat'], row['lon'])).km,
            axis=1
        )
        df_filtered = df_filtered[df_filtered['distance'] <= radius_km]
        # Return unique vessels with their tracks
        candidates = []
        for mmsi, group in df_filtered.groupby('mmsi'):
            candidates.append({
                'mmsi': mmsi,
                'name': group.iloc[0]['name'],
                'track': group[['lat','lon','timestamp','speed','heading']].to_dict('records'),
                'avg_distance': group['distance'].mean()
            })
        return candidates