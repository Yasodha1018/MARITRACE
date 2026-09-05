import { motion } from 'framer-motion';
import { FaTint, FaCheckCircle, FaExclamationTriangle, FaShip } from 'react-icons/fa';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import MapComponent from '../common/Map';

// Dummy data
const stats = [
  { label: 'Spill Area', value: '14.7 km²', icon: <FaTint />, color: 'text-bright-teal' },
  { label: 'Confidence', value: '94%', icon: <FaCheckCircle />, color: 'text-green-400' },
  { label: 'Severity', value: 'HIGH', icon: <FaExclamationTriangle />, color: 'text-rust' },
  { label: 'Vessels Detected', value: '8', icon: <FaShip />, color: 'text-ice' },
];

const chartData = [
  { time: '00:00', area: 0 },
  { time: '02:00', area: 2.1 },
  { time: '04:00', area: 5.3 },
  { time: '06:00', area: 8.7 },
  { time: '08:00', area: 12.4 },
  { time: '10:00', area: 14.7 },
];

const recentIncidents = [
  { id: 1, name: 'Arabian Sea Spill', date: '2025-09-04', severity: 'HIGH', area: '14.7 km²' },
  { id: 2, name: 'Bay of Bengal Leak', date: '2025-09-03', severity: 'MEDIUM', area: '8.2 km²' },
  { id: 3, name: 'Gulf of Mannar Slick', date: '2025-09-02', severity: 'LOW', area: '2.1 km²' },
];

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl font-bold text-ice flex items-center gap-2"
      >
        <FaShip className="text-bright-teal" /> Oil Spill Intelligence Dashboard
      </motion.h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s, idx) => (
          <motion.div
            key={s.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-deep-cyan/70 backdrop-blur-sm p-5 rounded-2xl shadow-lg border border-bright-teal/20 hover:shadow-bright-teal/20 transition-all duration-300"
          >
            <div className="flex items-center justify-between">
              <span className="text-ice text-sm">{s.label}</span>
              <span className={`text-2xl ${s.color}`}>{s.icon}</span>
            </div>
            <div className="text-3xl font-bold text-white mt-2">{s.value}</div>
          </motion.div>
        ))}
      </div>

      {/* Map & Chart Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 bg-deep-cyan/70 backdrop-blur-sm p-4 rounded-2xl border border-bright-teal/20">
          <h2 className="text-xl font-semibold text-ice mb-3">Current Incident Map</h2>
          <div className="h-[400px] rounded-xl overflow-hidden">
            <MapComponent center={[20, 70]} spillPolygon={[[20,70],[20.5,70.5],[20,71]]} vessels={[]} />
          </div>
        </div>
        <div className="bg-deep-cyan/70 backdrop-blur-sm p-4 rounded-2xl border border-bright-teal/20">
          <h2 className="text-xl font-semibold text-ice mb-3">Spill Growth</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#0FA4AF30" />
              <XAxis dataKey="time" stroke="#AFDDE5" />
              <YAxis stroke="#AFDDE5" />
              <Tooltip contentStyle={{ backgroundColor: '#024950', border: 'none' }} />
              <Line type="monotone" dataKey="area" stroke="#0FA4AF" strokeWidth={3} dot={{ fill: '#0FA4AF' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Incidents */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-deep-cyan/70 backdrop-blur-sm p-5 rounded-2xl border border-bright-teal/20"
      >
        <h2 className="text-xl font-semibold text-ice mb-4">Recent Incidents</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="text-ice/70 border-b border-bright-teal/20">
              <tr>
                <th className="py-2">Incident</th>
                <th>Date</th>
                <th>Severity</th>
                <th>Area</th>
              </tr>
            </thead>
            <tbody>
              {recentIncidents.map((inc) => (
                <tr key={inc.id} className="border-b border-bright-teal/10 hover:bg-bright-teal/5">
                  <td className="py-2 font-medium">{inc.name}</td>
                  <td>{inc.date}</td>
                  <td>
                    <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                      inc.severity === 'HIGH' ? 'bg-rust/30 text-rust' :
                      inc.severity === 'MEDIUM' ? 'bg-yellow-500/30 text-yellow-400' :
                      'bg-green-500/30 text-green-400'
                    }`}>
                      {inc.severity}
                    </span>
                  </td>
                  <td>{inc.area}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
}