# Smart Expense Analyzer

A full-stack application for uploading, analyzing, and tracking expenses with automatic anomaly detection.

## Description

Upload CSV files containing your expenses and get instant insights with interactive charts, spending breakdowns by category, time-based trends, and automatic detection of unusual expenses using statistical analysis.

## Features

- CSV file upload with validation
- Interactive dashboard with charts (Pie & Line)
- Automatic anomaly detection (2-sigma statistical method)
- Spending breakdown by category and date
- Professional dark-themed UI
- Type-safe code (TypeScript + Pydantic)

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, PostgreSQL/SQLite, Pydantic, Python 3.8+

**Frontend:** React 18, TypeScript, Vite, Axios, Recharts

## Setup

### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## CSV Format

Your CSV file must contain these columns:

```csv
date,category,amount,description
2026-01-01,Food,25.5,Lunch
2026-01-02,Transport,10,Taxi
2026-01-03,Shopping,200,Shoes
```

## Usage

1. Start backend: `python main.py` (in backend folder)
2. Start frontend: `npm run dev` (in frontend folder)
3. Open http://localhost:5173
4. Upload a CSV file
5. View analytics and anomalies on the dashboard

## Environment Variables

**Backend (.env):**
```
DATABASE_URL=sqlite:///./expenses.db
API_PORT=8000
```

**Frontend (.env):**
```
VITE_API_BASE_URL=http://localhost:8000
```

For PostgreSQL, update `DATABASE_URL` in backend/.env:
```
DATABASE_URL=postgresql+psycopg://username:password@host:5432/dbname
```
