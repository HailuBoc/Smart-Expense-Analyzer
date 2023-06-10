"""
Anomaly Detection Module

This module implements statistical anomaly detection for expense data.
Uses a simple but effective method based on standard deviation to identify
unusual expenses that deviate significantly from normal spending patterns.

Algorithm:
1. Calculate the mean (average) of all expense amounts
2. Calculate the standard deviation (measure of spread)
3. Set threshold = mean + (2 × standard deviation)
4. Mark any expense > threshold as an anomaly

This approach:
- Works well with small to medium datasets
- Is interpretable and explainable
- Requires no external ML libraries
- Performs well for expense data with typical distributions
"""

from models import Expense
from sqlalchemy.orm import Session

def detect_anomalies(db: Session):
    """
    Detect and flag anomalous expenses in the database.
    
    Uses statistical method to identify expenses that deviate significantly
    from normal spending patterns. Expenses are marked as anomalies if they
    exceed the threshold of (mean + 2 * standard_deviation).
    
    The 2-sigma rule means approximately 95% of normal expenses will be
    within the threshold, so flagged items are genuinely unusual.
    
    Args:
        db (Session): SQLAlchemy database session
        
    Returns:
        None (modifies database in-place)
        
    Note:
        - Requires at least 3 expenses to calculate meaningful statistics
        - Updates the is_anomaly flag for all expenses
        - Commits changes to the database
    """
    # Retrieve all expenses from database
    expenses = db.query(Expense).all()
    
    # Need at least 3 data points for meaningful statistics
    if len(expenses) < 3:
        return
    
    # Extract all amounts for statistical calculation
    amounts = [e.amount for e in expenses]
    
    # Calculate mean (average) expense amount
    mean = sum(amounts) / len(amounts)
    
    # Calculate variance (average squared deviation from mean)
    variance = sum((x - mean) ** 2 for x in amounts) / len(amounts)
    
    # Calculate standard deviation (square root of variance)
    # Measures how spread out the amounts are from the mean
    std_dev = variance ** 0.5
    
    # Set anomaly threshold at mean + 2 standard deviations
    # This is the 2-sigma rule: ~95% of normal data falls within this range
    threshold = mean + (2 * std_dev)
    
    # Mark each expense as anomaly or normal based on threshold
    for expense in expenses:
        expense.is_anomaly = expense.amount > threshold
    
    # Persist changes to database
    db.commit()
