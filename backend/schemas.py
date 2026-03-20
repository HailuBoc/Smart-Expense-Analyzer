from pydantic import BaseModel
from datetime import date
from typing import Dict

class ExpenseResponse(BaseModel):
    id: str
    date: date
    category: str
    amount: float
    description: str
    is_anomaly: bool
    
    class Config:
        from_attributes = True

class AnomalyResponse(BaseModel):
    id: str
    date: date
    category: str
    amount: float
    description: str
    
    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    total: float
    by_category: Dict[str, float]
    by_date: Dict[str, float]
