"""
Quick test to verify UUID serialization fix for Pydantic schemas.
This test ensures that UUID objects are properly converted to strings
in API responses, fixing the ResponseValidationError.
"""

from schemas import ExpenseResponse, AnomalyResponse
from uuid import UUID
from datetime import date
import json

def test_expense_response_uuid_conversion():
    """Test that ExpenseResponse properly converts UUID to string."""
    test_uuid = UUID('550e8400-e29b-41d4-a716-446655440000')
    
    # Create response with UUID object
    response = ExpenseResponse(
        id=test_uuid,
        date=date(2026, 1, 1),
        category='Food',
        amount=25.5,
        description='Lunch',
        is_anomaly=False
    )
    
    # Verify ID is converted to string
    assert isinstance(response.id, str), "ID should be a string"
    assert response.id == '550e8400-e29b-41d4-a716-446655440000', "UUID should be properly converted"
    
    # Verify JSON serialization works
    json_data = response.model_dump_json()
    parsed = json.loads(json_data)
    assert isinstance(parsed['id'], str), "JSON serialized ID should be a string"
    
    print("✓ ExpenseResponse UUID conversion works correctly")

def test_anomaly_response_uuid_conversion():
    """Test that AnomalyResponse properly converts UUID to string."""
    test_uuid = UUID('550e8400-e29b-41d4-a716-446655440001')
    
    # Create response with UUID object
    response = AnomalyResponse(
        id=test_uuid,
        date=date(2026, 1, 3),
        category='Shopping',
        amount=200.0,
        description='Shoes'
    )
    
    # Verify ID is converted to string
    assert isinstance(response.id, str), "ID should be a string"
    assert response.id == '550e8400-e29b-41d4-a716-446655440001', "UUID should be properly converted"
    
    # Verify JSON serialization works
    json_data = response.model_dump_json()
    parsed = json.loads(json_data)
    assert isinstance(parsed['id'], str), "JSON serialized ID should be a string"
    
    print("✓ AnomalyResponse UUID conversion works correctly")

def test_string_id_passthrough():
    """Test that string IDs are passed through unchanged."""
    string_id = '550e8400-e29b-41d4-a716-446655440002'
    
    response = ExpenseResponse(
        id=string_id,
        date=date(2026, 1, 2),
        category='Transport',
        amount=10.0,
        description='Taxi',
        is_anomaly=False
    )
    
    assert response.id == string_id, "String ID should pass through unchanged"
    print("✓ String ID passthrough works correctly")

if __name__ == '__main__':
    test_expense_response_uuid_conversion()
    test_anomaly_response_uuid_conversion()
    test_string_id_passthrough()
    print("\n✅ All UUID serialization tests passed!")
    print("✅ The ResponseValidationError should now be fixed!")
