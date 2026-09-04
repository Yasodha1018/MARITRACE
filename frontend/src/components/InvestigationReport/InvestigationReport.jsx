import { useState } from 'react';
import { generateReport } from '../../services/api';

const InvestigationReport = () => {
  const [report, setReport] = useState(null);

  const handleGenerate = async () => {
    const data = await generateReport(1);
    setReport(data);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-ice">Investigation Report</h1>
      <button onClick={handleGenerate} className="bg-bright-teal text-dark-teal px-6 py-2 rounded-lg mb-6">
        Generate Report
      </button>
      {report && (
        <div className="bg-deep-cyan p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold text-ice">Incident Report</h2>
          <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(report, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default InvestigationReport;