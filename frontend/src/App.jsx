import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import Dashboard from './components/Dashboard/Dashboard';
import SatelliteAnalysis from './components/SatelliteAnalysis/SatelliteAnalysis';
import DriftAnalysis from './components/DriftAnalysis/DriftAnalysis';
import VesselAttribution from './components/VesselAttribution/VesselAttribution';
import InvestigationReport from './components/InvestigationReport/InvestigationReport';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-dark-teal text-white">
        <Navbar />
        <div className="container mx-auto px-4 py-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/satellite" element={<SatelliteAnalysis />} />
            <Route path="/drift" element={<DriftAnalysis />} />
            <Route path="/vessels" element={<VesselAttribution />} />
            <Route path="/investigation" element={<InvestigationReport />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;