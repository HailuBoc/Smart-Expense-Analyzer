import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Expense {
  id: string;
  date: string;
  category: string;
  amount: number;
  description: string;
  is_anomaly: boolean;
}

export interface Summary {
  total: number;
  by_category: Record<string, number>;
  by_date: Record<string, number>;
}

export interface Anomaly {
  id: string;
  date: string;
  category: string;
  amount: number;
  description: string;
}

export const uploadCSV = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getExpenses = async (): Promise<Expense[]> => {
  const response = await api.get('/expenses');
  return response.data;
};

export const getSummary = async (): Promise<Summary> => {
  const response = await api.get('/summary');
  return response.data;
};

export const getAnomalies = async (): Promise<Anomaly[]> => {
  const response = await api.get('/anomalies');
  return response.data;
};
