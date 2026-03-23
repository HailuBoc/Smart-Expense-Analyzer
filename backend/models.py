"""
Database Models for Smart Expense Analyzer

This module defines the SQLAlchemy ORM models for the application.
Currently contains the Expense model which represents a single expense entry.
"""

from sqlalchemy import Column, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import date

# Create declarative base for all models
Base = declarative_base()

class Expense(Base):
    """
    Expense model representing a single expense entry.
    
    Attributes:
        id (UUID): Unique identifier for the expense (primary key)
        date (Date): Date of the expense in YYYY-MM-DD format
        category (String): Category of the expense (e.g., Food, Transport, Shopping)
        amount (Float): Amount spent in the expense
        description (String): Description or notes about the expense
        is_anomaly (Boolean): Flag indicating if this expense is an anomaly
        
    Indexes:
        - date: For efficient time-based queries
        - category: For category-based aggregations
        - is_anomaly: For quick anomaly retrieval
    """
    __tablename__ = "expenses"
    
    # Primary key: UUID generated automatically
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Expense date - indexed for time-based queries
    date = Column(Date, nullable=False, index=True)
    
    # Expense category - indexed for category grouping
    category = Column(String, nullable=False, index=True)
    
    # Expense amount
    amount = Column(Float, nullable=False)
    
    # Expense description
    description = Column(String, nullable=False)
    
    # Anomaly flag - indexed for quick anomaly retrieval
    is_anomaly = Column(Boolean, default=False, index=True)
