import { useState } from 'react';
import { motion } from 'framer-motion';
import { FaWind, FaMapMarkedAlt } from 'react-icons/fa';
import MapComponent from '../common/Map';

export default function DriftAnalysis() {
  const [origin, setOrigin] = useState({ lat: 20, lon: 70 });
  const [trajectory, setTrajectory] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTrace = async () => {
    setLoading(true);
    setTimeout(() => {
      setTrajectory({
        forward: [[20,70],[20.2,70.3],[20.5,70.6]],
        backward: [[20,70],[19.8,69.7],[19.5,69.4]],
        origin: [19.5, 69.4],
        origin_confidence: 82,
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl font-bold text-ice flex items-center gap-2"
      >
        <FaWind className="text-bright-teal" /> Drift Analysis
      </motion.h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 bg-deep-cyan/70 backdrop-blur-sm p-6 rounded-2xl border border-bright-teal/20">
          <h2 className="text-xl font-semibold text-ice mb-4">Parameters</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-ice/70 text-sm">Latitude</label>
              <input
                type="number"
                value={origin.lat}
                onChange={(e) => setOrigin({ ...origin, lat: parseFloat(e.target.value) })}
                className="w-full bg-dark-teal/60 text-white p-2 rounded-lg border border-bright-teal/30 focus:border-bright-teal outline-none"
              />
            </div>
            <div>
              <label className="block text-ice/70 text-sm">Longitude</label>
              <input
                type="number"
                value={origin.lon}
                onChange={(e) => setOrigin({ ...origin, lon: parseFloat(e.target.value) })}
                className="w-full bg-dark-teal/60 text-white p-2 rounded-lg border border-bright-teal/30 focus:border-bright-teal outline-none"
              />
            </div>
            <button
              onClick={handleTrace}
              disabled={loading}
              className="w-full bg-bright-teal text-dark-teal py-3 rounded-xl font-bold transition-all hover:bg-bright-teal/80 disabled:opacity-50"
            >
              {loading ? 'Tracing...' : 'Trace Drift'}
            </button>
          </div>
          {trajectory && (
            <div className="mt-4 p-3 bg-dark-teal/40 rounded-lg">
              <p className="text-ice/70 text-sm">Origin Confidence</p>
              <p className="text-2xl font-bold text-bright-teal">{trajectory.origin_confidence}%</p>
              <p className="text-ice/70 text-sm mt-2">Estimated Origin</p>
              <p className="text-white">({trajectory.origin[0].toFixed(4)}, {trajectory.origin[1].toFixed(4)})</p>
            </div>
          )}
        </div>

        <div className="lg:col-span-2 bg-deep-cyan/70 backdrop-blur-sm p-4 rounded-2xl border border-bright-teal/20">
          <h2 className="text-xl font-semibold text-ice mb-3 flex items-center gap-2">
            <FaMapMarkedAlt className="text-bright-teal" /> Drift Map
          </h2>
          <div className="h-[400px] rounded-xl overflow-hidden">
            <MapComponent
              center={[origin.lat, origin.lon]}
              spillPolygon={[]}
              driftPath={trajectory?.forward || []}
              vessels={[]}
            />
          </div>
          {trajectory && (
            <div className="mt-3 flex justify-between text-sm text-ice/70">
              <span>Backward: {trajectory.backward.length} steps</span>
              <span>Forward: {trajectory.forward.length} steps</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}