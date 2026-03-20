from models import Expense
from sqlalchemy.orm import Session

def detect_anomalies(db: Session):
    """Detect anomalies using simple statistical method"""
    expenses = db.query(Expense).all()
    
    if len(expenses) < 3:
        return
    
    # Simple statistical anomaly detection (no sklearn needed)
    amounts = [e.amount for e in expenses]
    mean = sum(amounts) / len(amounts)
    
    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in amounts) / len(amounts)
    std_dev = variance ** 0.5
    
    # Mark as anomaly if amount is more than 2 std devs from mean
    threshold = mean + (2 * std_dev)
    
    for expense in expenses:
        expense.is_anomaly = expense.amount > threshold
    
    db.commit()
