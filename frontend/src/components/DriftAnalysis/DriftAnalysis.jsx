import { useState } from 'react';
import { hindcast } from '../../services/api';
import MapComponent from '../common/Map';

const DriftAnalysis = () => {
  const [origin, setOrigin] = useState({ lat: 20, lon: 70 });
  const [trajectory, setTrajectory] = useState(null);

  const handleTrace = async () => {
    const data = await hindcast(origin.lat, origin.lon, 20);
    setTrajectory(data);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-ice">Drift Analysis</h1>
      <div className="bg-deep-cyan p-4 rounded-lg shadow-lg">
        <div className="flex space-x-4">
          <input type="number" placeholder="Lat" value={origin.lat} onChange={(e) => setOrigin({...origin, lat: parseFloat(e.target.value)})} className="bg-dark-teal text-white p-2 rounded" />
          <input type="number" placeholder="Lon" value={origin.lon} onChange={(e) => setOrigin({...origin, lon: parseFloat(e.target.value)})} className="bg-dark-teal text-white p-2 rounded" />
          <button onClick={handleTrace} className="bg-bright-teal text-dark-teal px-4 py-2 rounded">Trace Drift</button>
        </div>
      </div>
      {trajectory && (
        <div className="mt-6 bg-deep-cyan p-4 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold text-ice">Trajectory</h2>
          <p>Origin: ({trajectory.origin[0].toFixed(4)}, {trajectory.origin[1].toFixed(4)})</p>
          <p>Confidence: {trajectory.origin_confidence}%</p>
          <MapComponent center={[origin.lat, origin.lon]} driftPath={trajectory.forward} />
        </div>
      )}
    </div>
  );
};

export default DriftAnalysis;