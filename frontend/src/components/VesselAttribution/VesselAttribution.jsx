import { useState } from 'react';
import { motion } from 'framer-motion';
import { FaShip, FaTrophy, FaInfoCircle } from 'react-icons/fa';

export default function VesselAttribution() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleRank = async () => {
    setLoading(true);
    setTimeout(() => {
      setCandidates([
        { vessel_id: '123456789', vessel_name: 'Tanker Alpha', total_score: 91, components: { proximity: 85, temporal: 80, trajectory: 75, drift: 70, behavior: 65 }, evidence: ['Close to origin', 'Present during spill window'] },
        { vessel_id: '987654321', vessel_name: 'Cargo Bravo', total_score: 68, components: { proximity: 70, temporal: 65, trajectory: 60, drift: 55, behavior: 50 }, evidence: ['Moderate proximity', 'Trajectory intersects origin'] },
        { vessel_id: '456789123', vessel_name: 'Fishing Charlie', total_score: 44, components: { proximity: 40, temporal: 45, trajectory: 50, drift: 40, behavior: 35 }, evidence: ['Far from origin', 'AIS anomaly detected'] },
      ]);
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
        <FaShip className="text-bright-teal" /> Vessel Attribution
      </motion.h1>

      <button
        onClick={handleRank}
        disabled={loading}
        className="bg-bright-teal text-dark-teal px-8 py-3 rounded-xl font-bold transition-all hover:bg-bright-teal/80 disabled:opacity-50"
      >
        {loading ? 'Ranking...' : 'Rank Vessels'}
      </button>

      {candidates.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-4"
        >
          {candidates.map((c, idx) => (
            <motion.div
              key={c.vessel_id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="bg-deep-cyan/70 backdrop-blur-sm p-5 rounded-2xl border border-bright-teal/20 hover:border-bright-teal/50 transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {idx === 0 && <FaTrophy className="text-yellow-400 text-2xl" />}
                  <span className="text-lg font-bold text-white">{c.vessel_name}</span>
                  <span className="text-sm text-ice/70">({c.vessel_id})</span>
                </div>
                <span className={`text-2xl font-bold ${c.total_score > 80 ? 'text-green-400' : c.total_score > 60 ? 'text-yellow-400' : 'text-red-400'}`}>
                  {c.total_score}%
                </span>
              </div>
              <div className="mt-2 grid grid-cols-5 gap-2 text-sm">
                {Object.entries(c.components).map(([key, val]) => (
                  <div key={key} className="bg-dark-teal/40 p-2 rounded-lg text-center">
                    <span className="text-ice/70 block text-xs">{key}</span>
                    <span className="text-white">{val}%</span>
                  </div>
                ))}
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {c.evidence.map((e) => (
                  <span key={e} className="bg-bright-teal/20 text-bright-teal px-3 py-1 rounded-full text-xs flex items-center gap-1">
                    <FaInfoCircle className="text-xs" /> {e}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}