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

### Docker Setup

**Prerequisites:** Docker and Docker Compose installed

**Option 1: Full Stack with Docker Compose (Recommended)**

```bash
# Create .env file for database configuration
cat > .env << EOF
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=expenses_db
EOF

# Start all services (backend, frontend, PostgreSQL)
docker-compose up -d

# Access the app:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Option 2: Backend Only with Docker**

```bash
# Build the image
docker build -t expense-analyzer .

# Run with SQLite (development)
docker run -p 8000:8000 expense-analyzer

# Run with PostgreSQL (production)
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg://user:password@host:5432/dbname \
  expense-analyzer
```

**Stop Docker Services**

```bash
docker-compose down
```

**View Logs**

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

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

## Anomaly Detection Approach

The app uses a **statistical anomaly detection method** based on the 2-sigma rule:

1. **Calculate Statistics**: Computes mean and standard deviation of all expense amounts
2. **Set Threshold**: Threshold = Mean + (2 × Standard Deviation)
3. **Flag Anomalies**: Any expense exceeding the threshold is marked as anomalous
4. **Interpretation**: ~95% of normal expenses fall within this range, so flagged items are genuinely unusual

**Why this approach?**
- No external ML libraries needed (lightweight and fast)
- Interpretable and explainable results
- Works well with small to medium datasets
- Automatically adapts to spending patterns

**Example:**
- Mean expense: $50
- Std Dev: $20
- Threshold: $50 + (2 × $20) = $90
- Expenses > $90 are flagged as anomalies

## Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER BROWSER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React Frontend (TypeScript + Vite)                  │   │
│  │  - UploadPage: CSV file upload                       │   │
│  │  - DashboardPage: Charts & anomalies display         │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬──────────────────────────────────────┘
                         │ HTTP/REST (Axios)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints:                                      │   │
│  │  - POST /upload → Parse CSV & store expenses        │   │
│  │  - GET /expenses → Retrieve all expenses            │   │
│  │  - GET /summary → Aggregate spending data           │   │
│  │  - GET /anomalies → Return flagged expenses         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Anomaly Detector (anomaly_detector.py):            │   │
│  │  1. Fetch all expenses from DB                      │   │
│  │  2. Calculate mean & std deviation                  │   │
│  │  3. Set threshold = mean + (2 × std_dev)            │   │
│  │  4. Mark expenses > threshold as anomalies          │   │
│  │  5. Update is_anomaly flag in database              │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬──────────────────────────────────────┘
                         │ SQLAlchemy ORM
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Expenses Table:                                     │   │
│  │  - id (UUID)                                         │   │
│  │  - date                                              │   │
│  │  - category                                          │   │
│  │  - amount                                            │   │
│  │  - description                                       │   │
│  │  - is_anomaly (boolean flag)                         │   │
│  │                                                      │   │
│  │  Supported: SQLite (dev) or PostgreSQL (prod)       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

DATA FLOW:
1. User uploads CSV file
2. Backend parses and validates each row
3. Expenses stored in database
4. Anomaly detector runs automatically
5. Frontend fetches summary, expenses, and anomalies
6. Dashboard displays charts and flagged items
```
