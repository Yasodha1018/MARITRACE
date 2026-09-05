import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

// ----- Pages (minimal) -----
function Dashboard() {
  return <h1 className="text-4xl text-center mt-10 text-ice">🌊 Maritrace Dashboard</h1>;
}
function Satellite() {
  return <SatelliteUpload />;
}
function Drift() {
  return <div className="text-white">Drift Analysis (coming soon)</div>;
}
function Vessels() {
  return <div className="text-white">Vessel Attribution (coming soon)</div>;
}
function Report() {
  return <div className="text-white">Investigation Report (coming soon)</div>;
}

// ----- Satellite Upload Component (with API call) -----
import { useState } from 'react';
import axios from 'axios';

function SatelliteUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = (e) => setFile(e.target.files[0]);

  const handleDetect = async () => {
    if (!file) return alert('Please select an image');
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('http://localhost:8000/api/v1/detection/detect', formData);
      setResult(res.data);
    } catch (err) {
      alert('Error: ' + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="text-white">
      <h2 className="text-2xl font-bold mb-4">Satellite Image Upload</h2>
      <input type="file" accept="image/*" onChange={handleUpload} className="mb-4 block" />
      <button onClick={handleDetect} className="bg-bright-teal text-dark-teal px-4 py-2 rounded" disabled={loading}>
        {loading ? 'Detecting...' : 'Detect Spill'}
      </button>
      {result && (
        <div className="mt-4 p-4 bg-deep-cyan rounded">
          <p>Probability: {result.spill_probability?.toFixed(2)}%</p>
          <p>Area: {result.area_km2?.toFixed(2)} km²</p>
          <p>Severity: {result.severity}</p>
          <p>Confidence: {result.confidence?.toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}

// ----- Navigation -----
function Navbar() {
  return (
    <nav className="bg-deep-cyan p-4">
      <div className="container mx-auto flex flex-wrap items-center gap-4 text-white">
        <Link to="/" className="font-bold text-xl">MARITRACE</Link>
        <Link to="/" className="hover:text-bright-teal">Dashboard</Link>
        <Link to="/satellite" className="hover:text-bright-teal">Satellite</Link>
        <Link to="/drift" className="hover:text-bright-teal">Drift</Link>
        <Link to="/vessels" className="hover:text-bright-teal">Vessels</Link>
        <Link to="/report" className="hover:text-bright-teal">Report</Link>
      </div>
    </nav>
  );
}

// ----- Main App -----
function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="container mx-auto p-4">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/satellite" element={<Satellite />} />
          <Route path="/drift" element={<Drift />} />
          <Route path="/vessels" element={<Vessels />} />
          <Route path="/report" element={<Report />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;