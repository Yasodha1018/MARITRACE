import { MapContainer, TileLayer, Polygon, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function MapComponent({ center, zoom = 7, spillPolygon, driftPath, vessels }) {
  return (
    <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }} className="rounded-xl">
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      />
      {spillPolygon && <Polygon positions={spillPolygon} color="#964734" fillColor="#964734" fillOpacity={0.4} />}
      {driftPath && <Polyline positions={driftPath} color="#0FA4AF" dashArray="5,5" />}
      {vessels && vessels.map((v) => (
        <Marker key={v.mmsi} position={[v.lat, v.lon]}>
          <Popup>{v.name}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}