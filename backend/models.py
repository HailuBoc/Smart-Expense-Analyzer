from sqlalchemy import Column, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import date

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    is_anomaly = Column(Boolean, default=False, index=True)
