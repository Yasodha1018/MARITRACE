import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { detectSpill } from '../../services/api';
import { motion } from 'framer-motion';

const SatelliteAnalysis = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const onDrop = (acceptedFiles) => setFile(acceptedFiles[0]);
  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  const handleDetect = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const data = await detectSpill(file);
      setResults(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-ice">Satellite Analysis</h1>
      <div className="bg-deep-cyan p-6 rounded-lg shadow-lg">
        <div {...getRootProps()} className="border-2 border-dashed border-bright-teal p-8 text-center cursor-pointer">
          <input {...getInputProps()} />
          {file ? <p className="text-ice">{file.name}</p> : <p className="text-ice">Drag & drop SAR image here, or click to select</p>}
        </div>
        <button
          onClick={handleDetect}
          disabled={!file || loading}
          className="mt-4 bg-bright-teal text-dark-teal px-6 py-2 rounded-lg font-bold disabled:opacity-50"
        >
          {loading ? 'Detecting...' : 'Detect Spill'}
        </button>
      </div>
      {results && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mt-6 bg-deep-cyan p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold text-ice">Detection Results</h2>
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div>Probability: {results.spill_probability}%</div>
            <div>Area: {results.area_km2} km²</div>
            <div>Severity: {results.severity}</div>
            <div>Confidence: {results.confidence}%</div>
          </div>
          <div className="mt-4">
            <h3 className="font-bold">Look-alike Classification</h3>
            <ul>
              {Object.entries(results.lookalike_classification).map(([key, val]) => (
                <li key={key}>{key}: {val}%</li>
              ))}
            </ul>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default SatelliteAnalysis;