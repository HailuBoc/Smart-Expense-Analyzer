"""
Pydantic Schemas for Request/Response Validation

This module defines the Pydantic models used for validating
API requests and responses. These schemas ensure type safety
and provide automatic documentation in Swagger UI.
"""

from pydantic import BaseModel, field_validator
from datetime import date
from typing import Dict
from uuid import UUID

class ExpenseResponse(BaseModel):
    """
    Response schema for a single expense.
    
    Attributes:
        id: Unique identifier (UUID converted to string)
        date: Date of the expense
        category: Expense category
        amount: Amount spent
        description: Expense description
        is_anomaly: Whether this expense is flagged as anomaly
    """
    id: str
    date: date
    category: str
    amount: float
    description: str
    is_anomaly: bool
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        """Convert UUID objects to strings for JSON serialization."""
        if isinstance(v, UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True

class AnomalyResponse(BaseModel):
    """
    Response schema for an anomalous expense.
    
    Attributes:
        id: Unique identifier (UUID converted to string)
        date: Date of the expense
        category: Expense category
        amount: Amount spent
        description: Expense description
    """
    id: str
    date: date
    category: str
    amount: float
    description: str
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        """Convert UUID objects to strings for JSON serialization."""
        if isinstance(v, UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    """
    Response schema for spending summary and analytics.
    
    Attributes:
        total: Total spending across all expenses
        by_category: Dictionary mapping categories to total spending
        by_date: Dictionary mapping dates to daily spending
    """
    total: float
    by_category: Dict[str, float]
    by_date: Dict[str, float]
