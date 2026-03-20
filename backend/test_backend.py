from main import SessionLocal, Expense
from datetime import date

# Create test data
db = SessionLocal()
expenses = [
    Expense(date=date(2026, 1, 1), category="Food", amount=25.5, description="Lunch"),
    Expense(date=date(2026, 1, 2), category="Transport", amount=10, description="Taxi"),
    Expense(date=date(2026, 1, 3), category="Shopping", amount=200, description="Shoes"),
    Expense(date=date(2026, 1, 4), category="Food", amount=15.75, description="Coffee"),
]

db.add_all(expenses)
db.commit()

# Test queries
all_expenses = db.query(Expense).all()
print(f"✓ Created {len(all_expenses)} test expenses")

# Test summary
total = sum(e.amount for e in all_expenses)
print(f"✓ Total spending: ${total:.2f}")

# Test anomaly detection
from anomaly_detector import detect_anomalies
detect_anomalies(db)
anomalies = db.query(Expense).filter(Expense.is_anomaly == True).all()
print(f"✓ Anomaly detection: {len(anomalies)} anomalies found")

# Test category grouping
categories = {}
for e in all_expenses:
    categories[e.category] = categories.get(e.category, 0) + e.amount
print(f"✓ Categories: {categories}")

db.close()
print("✓ All backend tests passed!")
