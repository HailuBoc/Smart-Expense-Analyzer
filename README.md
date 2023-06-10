# Smart Expense Analyzer Dashboard

A production-ready full-stack application for uploading, analyzing, and tracking expenses with AI-powered anomaly detection.

## Overview

The Smart Expense Analyzer Dashboard is a web application that allows users to:
- Upload expense data via CSV files
- Visualize spending patterns with interactive charts
- Detect anomalous expenses using statistical analysis
- Track spending by category and time period

## Tech Stack

**Backend:**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23 (ORM)
- SQLite (Database)
- Pydantic 2.5.0 (Validation)
- Python 3.8+

**Frontend:**
- React 18.2.0
- TypeScript 5.3.3
- Vite 5.0.8
- Axios 1.6.2
- Recharts 2.10.3

## Project Structure

```
smart-expense-analyzer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── anomaly_detector.py     # Anomaly detection logic
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment config
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── api.ts              # Axios API client
│   │   ├── App.tsx             # Main app component
│   │   ├── main.tsx            # React entry point
│   │   └── index.css           # Styles
│   ├── package.json            # Node dependencies
│   ├── vite.config.ts          # Vite configuration
│   └── tsconfig.json           # TypeScript config
└── sample_expenses.csv         # Sample data for testing
```

## Features

- **CSV Upload**: Drag-and-drop file upload with validation
- **Database**: SQLite with automatic schema creation
- **Anomaly Detection**: Statistical method to identify outliers
- **Analytics Dashboard**: 
  - Summary cards (total spending, categories, anomalies)
  - Pie chart for category breakdown
  - Line chart for time trends
  - Anomalies table
- **Responsive Design**: Mobile-friendly UI
- **Error Handling**: Comprehensive validation and error messages
- **Type Safety**: TypeScript on frontend, Pydantic on backend

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /upload | Upload CSV file |
| GET | /expenses | Get all expenses |
| GET | /summary | Get spending summary |
| GET | /anomalies | Get detected anomalies |
| GET | /health | Health check |
| GET | /docs | Swagger API documentation |

## CSV Format

Your CSV file must contain these columns:

```csv
date,category,amount,description
2026-01-01,Food,25.5,Lunch
2026-01-02,Transport,10,Taxi
2026-01-03,Shopping,200,Shoes
```

## Installation & Setup

### Backend Setup

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows
# or
source venv/bin/activate     # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

**Note:** The backend supports both SQLite (default) and PostgreSQL. To use PostgreSQL, set the `DATABASE_URL` environment variable in `backend/.env`:

```
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/expenses_db
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. Start the backend server: `python main.py` (in backend folder)
2. Start the frontend dev server: `npm run dev` (in frontend folder)
3. Open http://localhost:5173 in your browser
4. Upload `sample_expenses.csv` or your own CSV file
5. View the dashboard with charts and analytics

## Testing

Run backend tests:

```bash
cd backend
python test_backend.py
```

## Key Features

✅ Drag-and-drop CSV upload
✅ Automatic anomaly detection
✅ Interactive charts (Pie & Line)
✅ Category-based spending breakdown
✅ Time-based trend analysis
✅ Responsive design
✅ Type-safe code (TypeScript + Pydantic)
✅ Production-ready error handling

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

## Production Build

**Frontend:**
```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/`

**Backend:**
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```
