import { MapContainer, TileLayer, Polygon, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapComponent = ({ center, zoom = 8, spillPolygon, driftPath, vessels }) => {
  return (
    <MapContainer center={center} zoom={zoom} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      {spillPolygon && <Polygon positions={spillPolygon} color="#964734" />}
      {driftPath && <Polyline positions={driftPath} color="#0FA4AF" />}
      {vessels && vessels.map((v) => (
        <Marker key={v.mmsi} position={[v.lat, v.lon]}>
          <Popup>{v.name}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapComponent;