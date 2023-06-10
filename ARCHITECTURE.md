# Architecture Overview

## System Design

The Smart Expense Analyzer is a full-stack web application with a clear separation of concerns between frontend and backend.

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TypeScript)            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Upload Page          │         Dashboard Page       │   │
│  │  - CSV Upload         │  - Summary Cards             │   │
│  │  - File Validation    │  - Pie Chart (Categories)    │   │
│  │  - Error Handling     │  - Line Chart (Trends)       │   │
│  │                       │  - Anomalies Table           │   │
│  └──────────────────────────────────────────────────────┘   │
│                              ↓                                │
│                         Axios API Client                      │
└─────────────────────────────────────────────────────────────┘
                              ↓ HTTP
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI + Python)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints                                       │   │
│  │  - POST /upload      (CSV file processing)           │   │
│  │  - GET /expenses     (Retrieve all expenses)         │   │
│  │  - GET /summary      (Spending analytics)            │   │
│  │  - GET /anomalies    (Flagged expenses)              │   │
│  │  - GET /health       (Health check)                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                              ↓                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Business Logic                                      │   │
│  │  - CSV Parsing & Validation                          │   │
│  │  - Anomaly Detection (Statistical)                   │   │
│  │  - Data Aggregation & Analytics                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                              ↓                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Data Layer (SQLAlchemy ORM)                         │   │
│  │  - Expense Model                                     │   │
│  │  - Database Queries                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓ SQL
┌─────────────────────────────────────────────────────────────┐
│              Database (PostgreSQL / SQLite)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  expenses table                                      │   │
│  │  - id (UUID)                                         │   │
│  │  - date (Date)                                       │   │
│  │  - category (String)                                 │   │
│  │  - amount (Float)                                    │   │
│  │  - description (String)                              │   │
│  │  - is_anomaly (Boolean)                              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. CSV Upload Flow
```
User selects CSV file
    ↓
Frontend validates file
    ↓
POST /upload with FormData
    ↓
Backend parses CSV
    ↓
Validate each row
    ↓
Store in database
    ↓
Run anomaly detection
    ↓
Return success response
    ↓
Frontend navigates to dashboard
```

### 2. Dashboard Data Flow
```
User views dashboard
    ↓
Frontend fetches data (parallel requests)
    ├─ GET /summary
    ├─ GET /expenses
    └─ GET /anomalies
    ↓
Backend queries database
    ↓
Aggregate and calculate analytics
    ↓
Return JSON responses
    ↓
Frontend renders charts and tables
```

## Technology Stack

### Frontend
- **Framework**: React 18.2.0
- **Language**: TypeScript 5.3.3
- **Build Tool**: Vite 5.0.8
- **HTTP Client**: Axios 1.6.2
- **Charts**: Recharts 2.10.3
- **Styling**: CSS3 with custom theme

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.48
- **Validation**: Pydantic 2.12.5
- **Database Driver**: psycopg 3.3.3

### Database
- **Primary**: PostgreSQL (production)
- **Alternative**: SQLite (development)

## Key Components

### Frontend Components
- **App.tsx**: Main application component with routing
- **UploadPage.tsx**: CSV upload interface
- **DashboardPage.tsx**: Analytics and visualization
- **api.ts**: Axios API client with typed responses

### Backend Modules
- **main.py**: FastAPI application and endpoints
- **models.py**: SQLAlchemy ORM models
- **schemas.py**: Pydantic request/response schemas
- **anomaly_detector.py**: Statistical anomaly detection

## Anomaly Detection Algorithm

Uses statistical method based on standard deviation:

```
1. Calculate mean of all expense amounts
2. Calculate standard deviation
3. Set threshold = mean + (2 × std_dev)
4. Mark expenses > threshold as anomalies
```

This approach:
- Requires no external ML libraries
- Works with small datasets
- Is interpretable and explainable
- Performs well for expense data

## Security Considerations

- CORS enabled for frontend origin only
- Input validation on all endpoints
- SQL injection prevention via ORM
- Type safety with TypeScript and Pydantic
- Environment variables for sensitive data

## Performance Optimizations

- Database indexes on frequently queried columns (date, category, is_anomaly)
- Connection pooling with SQLAlchemy
- Parallel API requests on frontend
- Efficient CSV parsing with Python's csv module
- Responsive UI with CSS Grid and Flexbox

## Scalability

### Current Limitations
- Single-threaded backend (can be scaled with Gunicorn workers)
- In-memory anomaly detection (suitable for <100k expenses)
- No caching layer

### Future Improvements
- Redis caching for frequently accessed data
- Database query optimization with pagination
- Background job processing for large uploads
- API rate limiting
- User authentication and authorization
