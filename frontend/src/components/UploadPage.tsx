import React, { useState } from 'react';
import { uploadCSV } from '../api';

interface UploadPageProps {
  onUploadSuccess: () => void;
}

export const UploadPage: React.FC<UploadPageProps> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setMessage(null);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile && droppedFile.name.endsWith('.csv')) {
      setFile(droppedFile);
      setMessage(null);
    } else {
      setMessage({ type: 'error', text: 'Please drop a CSV file' });
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setMessage({ type: 'error', text: 'Please select a file' });
      return;
    }

    setLoading(true);
    try {
      const response = await uploadCSV(file);
      setMessage({ type: 'success', text: response.data.message });
      setFile(null);
      setTimeout(() => onUploadSuccess(), 1500);
    } catch (error: any) {
      // Enhanced error handling with detailed messages
      let errorMsg = 'Upload failed';
      
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (typeof detail === 'string') {
          errorMsg = detail;
        } else if (detail.message) {
          errorMsg = detail.message;
        } else {
          errorMsg = JSON.stringify(detail);
        }
      } else if (error.message) {
        errorMsg = error.message;
      } else if (error.code === 'ERR_NETWORK') {
        errorMsg = 'Network error: Cannot reach the server. Check your internet connection and API URL.';
      } else if (error.code === 'ECONNABORTED') {
        errorMsg = 'Request timeout: Server took too long to respond.';
      }
      
      console.error('Upload error:', error);
      setMessage({ type: 'error', text: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-section">
      <h2>Upload Expenses CSV</h2>
      <p style={{ color: '#666', marginBottom: '20px', fontSize: '14px' }}>
        Upload a CSV file with columns: date, category, amount, description
      </p>

      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div
        className="upload-area"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input')?.click()}
      >
        <div style={{ fontSize: '40px', marginBottom: '10px' }}>📁</div>
        <p>Drag and drop your CSV file here</p>
        <p style={{ fontSize: '12px', color: '#999' }}>or click to select</p>
        <input
          id="file-input"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
        />
      </div>

      {file && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#1a1a1a', borderRadius: '6px', border: '1px solid #2a2a2a' }}>
          <p style={{ marginBottom: '10px', color: '#ffffff' }}>
            <strong>Selected file:</strong> {file.name}
          </p>
          <button
            className="upload-btn"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      )}

      <div style={{ marginTop: '30px', padding: '20px', background: '#1a1a1a', borderRadius: '6px', border: '1px solid #2a2a2a' }}>
        <h3 style={{ marginBottom: '10px', color: '#ffffff' }}>Sample CSV Format</h3>
        <pre style={{ fontSize: '12px', overflow: 'auto', color: '#ffffff', background: '#0d0d0d', padding: '15px', borderRadius: '4px', border: '1px solid #2a2a2a' }}>
{`date,category,amount,description
2026-01-01,Food,25.5,Lunch
2026-01-02,Transport,10,Taxi
2026-01-03,Shopping,200,Shoes`}
        </pre>
      </div>
    </div>
  );
};
