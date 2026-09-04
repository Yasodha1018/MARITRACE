import { motion } from 'framer-motion';
import MapComponent from '../common/Map';
import { useStore } from '../../store/useStore';

const Dashboard = () => {
  const { incident } = useStore();
  // Dummy data
  const stats = [
    { label: 'Spill Area', value: '14.7 km²' },
    { label: 'Confidence', value: '94%' },
    { label: 'Severity', value: 'HIGH' },
    { label: 'Vessels', value: '8' },
  ];

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
        {stats.map((s) => (
          <div key={s.label} className="bg-deep-cyan p-4 rounded-lg shadow-lg">
            <div className="text-sm text-ice">{s.label}</div>
            <div className="text-2xl font-bold text-bright-teal">{s.value}</div>
          </div>
        ))}
      </div>
      <div className="bg-deep-cyan p-4 rounded-lg shadow-lg">
        <MapComponent center={[20, 70]} spillPolygon={[[20,70],[21,71],[20,72]]} />
      </div>
    </div>
  );
};

export default Dashboard;