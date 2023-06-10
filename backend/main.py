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

# Load environment variables
load_dotenv()

# Database setup - use psycopg3 driver
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./expenses.db")
# Convert psycopg2 URLs to psycopg3 if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Expense Analyzer")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and parse CSV file"""
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
    """Get all expenses"""
    db = SessionLocal()
    expenses = db.query(Expense).all()
    db.close()
    return expenses

@app.get("/summary", response_model=SummaryResponse)
async def get_summary():
    """Get spending summary"""
    db = SessionLocal()
    expenses = db.query(Expense).all()
    db.close()
    
    if not expenses:
        return SummaryResponse(total=0, by_category={}, by_date={})
    
    total = sum(e.amount for e in expenses)
    
    by_category = {}
    for e in expenses:
        by_category[e.category] = by_category.get(e.category, 0) + e.amount
    
    by_date = {}
    for e in expenses:
        date_str = e.date.isoformat()
        by_date[date_str] = by_date.get(date_str, 0) + e.amount
    
    return SummaryResponse(total=total, by_category=by_category, by_date=by_date)

@app.get("/anomalies", response_model=list[AnomalyResponse])
async def get_anomalies():
    """Get anomalous expenses"""
    db = SessionLocal()
    anomalies = db.query(Expense).filter(Expense.is_anomaly == True).all()
    db.close()
    return anomalies

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
