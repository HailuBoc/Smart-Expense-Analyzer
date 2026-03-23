import React, { useState, useEffect } from 'react';
import { getSummary, getAnomalies, Summary, Anomaly } from '../api';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DashboardPageProps {
  refreshTrigger: number;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ refreshTrigger }) => {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, [refreshTrigger]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('Fetching dashboard data...');
      const [summaryData, anomaliesData] = await Promise.all([
        getSummary(),
        getAnomalies(),
      ]);
      console.log('Dashboard data fetched successfully:', { summaryData, anomaliesData });
      setSummary(summaryData);
      setAnomalies(anomaliesData);
    } catch (err: any) {
      console.error('Dashboard fetch error:', err);
      
      // Enhanced error message
      let errorMsg = 'Failed to load dashboard';
      
      if (err.response?.status === 404) {
        errorMsg = 'API endpoint not found. Check backend URL.';
      } else if (err.response?.status === 500) {
        errorMsg = 'Server error. Check backend logs.';
      } else if (err.code === 'ERR_NETWORK') {
        errorMsg = 'Network error: Cannot reach the server. Check your internet connection and backend URL.';
      } else if (err.message) {
        errorMsg = err.message;
      }
      
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px' }}>
        <div className="message error">
          {error}
        </div>
        <button
          className="upload-btn"
          onClick={fetchData}
          style={{ marginTop: '15px' }}
        >
          Retry
        </button>
        <p style={{ marginTop: '15px', color: '#999', fontSize: '12px' }}>
          Debug info: Check browser console (F12) for more details.
        </p>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="empty-state">
        <p>No data available. Upload a CSV file to get started.</p>
      </div>
    );
  }

  // Prepare chart data
  const categoryData = Object.entries(summary.by_category).map(([name, value]) => ({
    name,
    value: parseFloat((value as number).toFixed(2)),
  }));

  const dateData = Object.entries(summary.by_date)
    .sort(([dateA], [dateB]) => dateA.localeCompare(dateB))
    .map(([date, amount]) => ({
      date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      amount: parseFloat((amount as number).toFixed(2)),
    }));

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#fee140'];

  return (
    <div>
      {/* Summary Cards */}
      <div className="dashboard">
        <div className="card">
          <h3>Total Spending</h3>
          <div className="value">${summary.total.toFixed(2)}</div>
        </div>
        <div className="card">
          <h3>Categories</h3>
          <div className="value">{Object.keys(summary.by_category).length}</div>
        </div>
        <div className="card">
          <h3>Anomalies</h3>
          <div className="value">{anomalies.length}</div>
        </div>
      </div>

      {/* Charts */}
      {categoryData.length > 0 && (
        <div className="chart-container">
          <h3>Spending by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: $${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `$${(value as number).toFixed(2)}`} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {dateData.length > 0 && (
        <div className="chart-container">
          <h3>Spending Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dateData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip formatter={(value) => `$${(value as number).toFixed(2)}`} />
              <Legend />
              <Line
                type="monotone"
                dataKey="amount"
                stroke="#667eea"
                strokeWidth={2}
                dot={{ fill: '#667eea', r: 4 }}
                activeDot={{ r: 6 }}
                name="Daily Spending"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Anomalies Table */}
      {anomalies.length > 0 && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {anomalies.map((anomaly) => (
                <tr key={anomaly.id}>
                  <td>{new Date(anomaly.date).toLocaleDateString()}</td>
                  <td>{anomaly.category}</td>
                  <td>${anomaly.amount.toFixed(2)}</td>
                  <td>{anomaly.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {anomalies.length === 0 && (
        <div className="chart-container">
          <h3>Anomalies</h3>
          <div className="empty-state">
            <p>No anomalies detected in your expenses.</p>
          </div>
        </div>
      )}
    </div>
  );
};
