import { useState } from 'react';
import { motion } from 'framer-motion';
import { FaFilePdf, FaDownload } from 'react-icons/fa';

export default function InvestigationReport() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setTimeout(() => {
      setReport({
        incident_id: 'MS-2025-001',
        detection_time: '2025-09-04T08:30:00Z',
        location: '20.5, 70.2',
        spill_area: '14.7 km²',
        confidence: '94%',
        severity: 'HIGH',
        origin: '19.8, 69.7',
        origin_confidence: '82%',
        candidates: [
          { vessel: 'Tanker Alpha', score: 91, evidence: ['Proximity', 'Temporal match'] },
          { vessel: 'Cargo Bravo', score: 68, evidence: ['Trajectory similarity'] },
        ],
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
        <FaFilePdf className="text-bright-teal" /> Investigation Report
      </motion.h1>

      <button
        onClick={handleGenerate}
        disabled={loading}
        className="bg-bright-teal text-dark-teal px-8 py-3 rounded-xl font-bold transition-all hover:bg-bright-teal/80 disabled:opacity-50 flex items-center gap-2"
      >
        <FaDownload /> {loading ? 'Generating...' : 'Generate Report'}
      </button>

      {report && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-deep-cyan/70 backdrop-blur-sm p-6 rounded-2xl border border-bright-teal/20"
        >
          <h2 className="text-xl font-bold text-ice mb-4">Incident Report</h2>
          <div className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-2">
              <span className="text-ice/70">Incident ID</span>
              <span className="text-white">{report.incident_id}</span>
              <span className="text-ice/70">Detection Time</span>
              <span className="text-white">{report.detection_time}</span>
              <span className="text-ice/70">Location</span>
              <span className="text-white">{report.location}</span>
              <span className="text-ice/70">Spill Area</span>
              <span className="text-white">{report.spill_area}</span>
              <span className="text-ice/70">Confidence</span>
              <span className="text-white">{report.confidence}</span>
              <span className="text-ice/70">Severity</span>
              <span className={`font-bold ${report.severity === 'HIGH' ? 'text-rust' : 'text-yellow-400'}`}>{report.severity}</span>
              <span className="text-ice/70">Estimated Origin</span>
              <span className="text-white">{report.origin}</span>
              <span className="text-ice/70">Origin Confidence</span>
              <span className="text-white">{report.origin_confidence}</span>
            </div>
            <div className="mt-4">
              <h3 className="text-ice font-semibold mb-2">Potentially Associated Vessels</h3>
              {report.candidates.map((c, idx) => (
                <div key={idx} className="flex justify-between items-center bg-dark-teal/40 p-3 rounded-lg mb-2">
                  <span className="text-white">{c.vessel}</span>
                  <span className={`font-bold ${c.score > 80 ? 'text-green-400' : 'text-yellow-400'}`}>{c.score}%</span>
                  <span className="text-xs text-ice/70">{c.evidence.join(', ')}</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}