import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Navbar = () => {
  const links = [
    { to: '/', label: 'Dashboard' },
    { to: '/satellite', label: 'Satellite' },
    { to: '/drift', label: 'Drift' },
    { to: '/vessels', label: 'Vessels' },
    { to: '/investigation', label: 'Investigation' },
  ];
  return (
    <nav className="bg-deep-cyan p-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-2xl font-bold text-ice"
        >
          MARITRACE
        </motion.div>
        <ul className="flex space-x-6">
          {links.map((link) => (
            <li key={link.to}>
              <Link
                to={link.to}
                className="hover:text-bright-teal transition-colors duration-300"
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;