import React, { useState } from 'react';
import { UploadPage } from './components/UploadPage';
import { DashboardPage } from './components/DashboardPage';
import './index.css';

function App() {
  const [currentPage, setCurrentPage] = useState<'upload' | 'dashboard'>('upload');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = () => {
    setRefreshTrigger(prev => prev + 1);
    setCurrentPage('dashboard');
  };

  return (
    <div className="container">
      <div className="header">
        <h1>💰 Smart Expense Analyzer</h1>
        <p>Upload, analyze, and track your expenses with AI-powered anomaly detection</p>
      </div>

      <div className="nav-tabs">
        <button
          className={currentPage === 'upload' ? 'active' : ''}
          onClick={() => setCurrentPage('upload')}
        >
          📤 Upload
        </button>
        <button
          className={currentPage === 'dashboard' ? 'active' : ''}
          onClick={() => setCurrentPage('dashboard')}
        >
          📊 Dashboard
        </button>
      </div>

      {currentPage === 'upload' && <UploadPage onUploadSuccess={handleUploadSuccess} />}
      {currentPage === 'dashboard' && <DashboardPage refreshTrigger={refreshTrigger} />}
    </div>
  );
}

export default App;
