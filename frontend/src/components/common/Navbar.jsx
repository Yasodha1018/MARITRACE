import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaShip, FaSatellite, FaWind, FaShip as FaVessel, FaFileAlt } from 'react-icons/fa';

const navItems = [
  { path: '/', label: 'Dashboard', icon: <FaShip /> },
  { path: '/satellite', label: 'Satellite', icon: <FaSatellite /> },
  { path: '/drift', label: 'Drift', icon: <FaWind /> },
  { path: '/vessels', label: 'Vessels', icon: <FaVessel /> },
  { path: '/investigation', label: 'Report', icon: <FaFileAlt /> },
];

export default function Navbar() {
  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="bg-deep-cyan/80 backdrop-blur-md shadow-lg border-b border-bright-teal/20 sticky top-0 z-50"
    >
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="text-2xl font-bold text-ice flex items-center gap-2"
        >
          <FaShip className="text-bright-teal" />
          MARITRACE
        </motion.div>
        <ul className="flex space-x-1 md:space-x-4">
          {navItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className="flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-bright-teal/20 hover:text-bright-teal"
              >
                <span className="text-bright-teal">{item.icon}</span>
                <span className="hidden md:inline">{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </motion.nav>
  );
}