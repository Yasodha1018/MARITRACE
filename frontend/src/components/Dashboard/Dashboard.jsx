import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import MapComponent from '../common/Map';
import { useStore } from '../../store/useStore';
import { getIncidents, getActiveIncident } from '../../services/api';

const Dashboard = () => {
  const { incident, setIncident } = useStore();
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState([
    { label: 'Spill Area', value: '--' },
    { label: 'Confidence', value: '--' },
    { label: 'Severity', value: '--' },
    { label: 'Vessels', value: '--' },
  ]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getActiveIncident();
        if (data) {
          setIncident(data);
          setStats([
            { label: 'Spill Area', value: `${data.spill_area_km2?.toFixed(2) || '--'} km²` },
            { label: 'Confidence', value: `${data.confidence?.toFixed(0) || '--'}%` },
            { label: 'Severity', value: data.severity || '--' },
            { label: 'Vessels', value: data.vessel_count || '--' },
          ]);
        }
        const list = await getIncidents();
        setIncidents(list || []);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [setIncident]);

  return (
    <div>
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl font-bold mb-6 text-ice"
      >
        Dashboard
      </motion.h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {stats.map((s, idx) => (
          <motion.div
            key={s.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-deep-cyan p-4 rounded-lg shadow-lg"
          >
            <div className="text-sm text-ice">{s.label}</div>
            <div className="text-2xl font-bold text-bright-teal">{s.value}</div>
          </motion.div>
        ))}
      </div>
      
      <div className="bg-deep-cyan p-4 rounded-lg shadow-lg">
        <MapComponent 
          center={[20, 70]} 
          spillPolygon={incident?.polygon || [[20,70],[21,71],[20,72]]}
          vessels={incident?.vessels || []}
          driftPath={incident?.drift_path || []}
        />
      </div>
      
      {incidents.length > 0 && (
        <div className="mt-6 bg-deep-cyan p-4 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold text-ice mb-4">Recent Incidents</h2>
          <ul>
            {incidents.slice(0, 5).map((inc) => (
              <li key={inc.id} className="border-b border-bright-teal py-2">
                <div className="flex justify-between">
                  <span>{inc.name}</span>
                  <span className={`font-bold ${
                    inc.severity === 'HIGH' ? 'text-red-500' : 
                    inc.severity === 'MEDIUM' ? 'text-yellow-500' : 'text-green-500'
                  }`}>
                    {inc.severity}
                  </span>
                </div>
                <div className="text-sm text-ice">
                  {inc.detection_time} • {inc.spill_area_km2?.toFixed(2)} km²
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Dashboard;