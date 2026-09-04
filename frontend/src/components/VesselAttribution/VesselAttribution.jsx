import { useState } from 'react';
import { rankVessels } from '../../services/api';
import { motion } from 'framer-motion';

const VesselAttribution = () => {
  const [candidates, setCandidates] = useState([]);

  const handleRank = async () => {
    // Dummy parameters
    const data = await rankVessels(1, 20, 70, '2025-09-04T08:00:00Z', '2025-09-04T10:00:00Z');
    setCandidates(data.candidates);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-ice">Vessel Attribution</h1>
      <button onClick={handleRank} className="bg-bright-teal text-dark-teal px-6 py-2 rounded-lg mb-6">
        Rank Vessels
      </button>
      {candidates.length > 0 && (
        <div className="bg-deep-cyan p-4 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold text-ice">Ranked Candidates</h2>
          <ul>
            {candidates.map((c, idx) => (
              <motion.li
                key={c.vessel_id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="border-b border-bright-teal py-4"
              >
                <div className="flex justify-between">
                  <span className="font-bold">{c.vessel_name}</span>
                  <span className="text-bright-teal">{c.total_score}%</span>
                </div>
                <div className="text-sm text-ice">
                  {Object.entries(c.components).map(([k, v]) => `${k}: ${v.toFixed(0)}% `)}
                </div>
                <div className="text-xs text-ice mt-1">
                  Evidence: {c.evidence.join('; ')}
                </div>
              </motion.li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default VesselAttribution;