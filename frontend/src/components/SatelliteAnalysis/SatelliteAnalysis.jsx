import { useState } from 'react';
import axios from 'axios';

export default function SatelliteAnalysis() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDetect = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('http://localhost:8000/api/v1/detection/detect', formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert('Error: ' + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="text-white">
      <h2 className="text-2xl font-bold mb-4">Satellite Image Upload</h2>
      <input type="file" accept="image/*" onChange={handleUpload} className="mb-4" />
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