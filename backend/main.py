"""
Smart Expense Analyzer Backend API

This module implements the FastAPI backend for the Smart Expense Analyzer application.
It provides endpoints for:
- CSV file upload and processing
- Expense data retrieval and aggregation
- Anomaly detection and reporting
- Health checks

The backend supports both SQLite (development) and PostgreSQL (production) databases.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import csv
import io
from models import Base, Expense
from schemas import ExpenseResponse, SummaryResponse, AnomalyResponse
from anomaly_detector import detect_anomalies
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
# Supports both SQLite (default) and PostgreSQL
# DATABASE_URL format:
#   SQLite: sqlite:///./expenses.db
#   PostgreSQL: postgresql+psycopg://user:password@host:5432/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./expenses.db")

# Convert legacy psycopg2 URLs to psycopg3 format if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

# Create database engine with connection pooling
# pool_pre_ping=True ensures connections are valid before use
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Smart Expense Analyzer",
    description="API for uploading, analyzing, and tracking expenses with anomaly detection",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# Allows frontend to make requests to this backend
# In production, allow Vercel frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Local development
        "http://localhost:3000",      # Alternative local port
        "https://smart-expense-analyzer.vercel.app",  # Production frontend
        "*"  # Allow all origins in production (can be restricted later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    """
    Database session dependency for FastAPI.
    
    Provides a database session to route handlers and ensures
    proper cleanup after the request completes.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload and process a CSV file containing expense data.
    
    The CSV file must contain the following columns:
    - date: Date in YYYY-MM-DD format
    - category: Expense category (string)
    - amount: Expense amount (float)
    - description: Expense description (string)
    
    After successful upload:
    1. Each row is validated
    2. Valid expenses are stored in the database
    3. Anomaly detection is run on all expenses
    4. Results are returned to the client
    
    Args:
        file: CSV file uploaded by the client
        
    Returns:
        dict: Success message with count of uploaded expenses
        
    Raises:
        HTTPException: If file is invalid or contains errors
    """
    try:
        contents = await file.read()
        text = contents.decode('utf-8')
        reader = csv.DictReader(io.StringIO(text))
        
        # Validate columns
        if not reader.fieldnames:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        required_cols = {'date', 'category', 'amount', 'description'}
        if not required_cols.issubset(set(reader.fieldnames)):
            raise HTTPException(status_code=400, detail=f"CSV must contain columns: {required_cols}")
        
        db = SessionLocal()
        expenses = []
        errors = []
        
        for idx, row in enumerate(reader, start=2):
            try:
                # Parse date
                from datetime import datetime as dt
                date_obj = dt.strptime(row['date'].strip(), '%Y-%m-%d').date()
                
                expense = Expense(
                    date=date_obj,
                    category=str(row['category']).strip(),
                    amount=float(row['amount']),
                    description=str(row['description']).strip()
                )
                expenses.append(expense)
            except ValueError as e:
                errors.append(f"Row {idx}: {str(e)}")
            except Exception as e:
                errors.append(f"Row {idx}: {str(e)}")
        
        if errors:
            db.close()
            raise HTTPException(status_code=400, detail={"message": "Validation errors", "errors": errors})
        
        if not expenses:
            db.close()
            raise HTTPException(status_code=400, detail="No valid expenses found in CSV")
        
        # Add to database
        db.add_all(expenses)
        db.commit()
        
        # Run anomaly detection
        detect_anomalies(db)
        
        db.close()
        return {"message": f"Successfully uploaded {len(expenses)} expenses", "count": len(expenses)}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/expenses", response_model=list[ExpenseResponse])
async def get_expenses():
    """
    Retrieve all expenses from the database.
    
    Returns all expenses that have been uploaded, including:
    - Expense ID (UUID)
    - Date
    - Category
    - Amount
    - Description
    - Anomaly flag
    
    Returns:
        list[ExpenseResponse]: List of all expenses
    """
    db = SessionLocal()
    expenses = db.query(Expense).all()
    db.close()
    return expenses

@app.get("/summary", response_model=SummaryResponse)
async def get_summary():
    """
    Get spending summary and analytics.
    
    Calculates and returns:
    - Total spending across all expenses
    - Spending breakdown by category
    - Daily spending trends
    
    Returns:
        SummaryResponse: Aggregated spending data
    """
    db = SessionLocal()
    expenses = db.query(Expense).all()
    db.close()
    
    if not expenses:
        return SummaryResponse(total=0, by_category={}, by_date={})
    
    # Calculate total spending
    total = sum(e.amount for e in expenses)
    
    # Group spending by category
    by_category = {}
    for e in expenses:
        by_category[e.category] = by_category.get(e.category, 0) + e.amount
    
    # Group spending by date
    by_date = {}
    for e in expenses:
        date_str = e.date.isoformat()
        by_date[date_str] = by_date.get(date_str, 0) + e.amount
    
    return SummaryResponse(total=total, by_category=by_category, by_date=by_date)

@app.get("/anomalies", response_model=list[AnomalyResponse])
async def get_anomalies():
    """
    Retrieve expenses flagged as anomalies.
    
    Returns all expenses where is_anomaly is True.
    These are expenses that deviate significantly from normal spending patterns.
    
    Anomaly detection uses a statistical method:
    - Calculates mean and standard deviation of all amounts
    - Flags expenses > (mean + 2 * std_dev) as anomalies
    
    Returns:
        list[AnomalyResponse]: List of anomalous expenses
    """
    db = SessionLocal()
    anomalies = db.query(Expense).filter(Expense.is_anomaly == True).all()
    db.close()
    return anomalies

@app.get("/health")
async def health():
    """
    Health check endpoint.
    
    Used to verify that the API is running and responsive.
    Can be used for monitoring and load balancer health checks.
    
    Returns:
        dict: Status indicator
    """
    return {"status": "ok"}

if __name__ == "__main__":
    """
    Application entry point.
    
    Starts the Uvicorn ASGI server with the FastAPI application.
    Configuration:
    - Host: 0.0.0.0 (accessible from any network interface)
    - Port: Read from API_PORT environment variable (default: 8000)
    - Reload: Disabled in production
    - Log level: Adjusted based on environment
    """
    import uvicorn
    import os
    
    port = int(os.getenv("API_PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")
    debug = environment == "development"
    
    # Use appropriate log level based on environment
    log_level = "debug" if debug else "info"
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level=log_level
    )
