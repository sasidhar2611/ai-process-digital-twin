import pytest
import pandas as pd
from src.data.validator import TimestampValidator

def test_valid_chronological_sequence():
    """Test that valid chronological sequences pass all rules."""
    validator = TimestampValidator()
    
    df_orders = pd.DataFrame({
        "order_id": ["O1"],
        "order_status": ["delivered"],
        "order_purchase_timestamp": pd.to_datetime(["2023-01-01 10:00:00"]),
        "order_approved_at": pd.to_datetime(["2023-01-01 11:00:00"]),
        "order_delivered_carrier_date": pd.to_datetime(["2023-01-02 10:00:00"]),
        "order_delivered_customer_date": pd.to_datetime(["2023-01-05 10:00:00"]),
        "order_estimated_delivery_date": pd.to_datetime(["2023-01-10 00:00:00"])
    })
    
    results = validator.validate_orders_timestamps(df_orders)
    
    assert results["rules"]["Rule A"]["failed"] == 0
    assert results["rules"]["Rule B"]["failed"] == 0
    assert results["rules"]["Rule C"]["failed"] == 0
    assert results["rules"]["Rule D"]["failed"] == 0
    assert results["rules"]["Rule E"]["failed"] == 0
    
    assert results["rules"]["Rule A"]["passed"] == 1
    
def test_invalid_chronological_sequence():
    """Test that invalid chronological sequence is detected."""
    validator = TimestampValidator()
    
    df_orders = pd.DataFrame({
        "order_id": ["O1"],
        "order_status": ["delivered"],
        "order_purchase_timestamp": pd.to_datetime(["2023-01-01 12:00:00"]),
        "order_approved_at": pd.to_datetime(["2023-01-01 10:00:00"]),  # Invalid: approved before purchase
        "order_delivered_carrier_date": pd.to_datetime(["2023-01-02 10:00:00"]),
        "order_delivered_customer_date": pd.to_datetime(["2023-01-05 10:00:00"]),
        "order_estimated_delivery_date": pd.to_datetime(["2023-01-10 00:00:00"])
    })
    
    results = validator.validate_orders_timestamps(df_orders)
    assert results["rules"]["Rule A"]["failed"] == 1
    assert results["rules"]["Rule A"]["passed"] == 0

def test_missing_timestamps_handled():
    """Missing timestamps are handled without crashing and properly accounted for."""
    validator = TimestampValidator()
    
    df_orders = pd.DataFrame({
        "order_id": ["O1", "O2"],
        "order_status": ["invoiced", "canceled"],
        "order_purchase_timestamp": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-02 10:00:00"]),
        "order_approved_at": pd.to_datetime(["2023-01-01 11:00:00", pd.NaT]),
        "order_delivered_carrier_date": pd.to_datetime([pd.NaT, pd.NaT]),
        "order_delivered_customer_date": pd.to_datetime([pd.NaT, pd.NaT]),
        "order_estimated_delivery_date": pd.to_datetime(["2023-01-10 00:00:00", "2023-01-11 00:00:00"])
    })
    
    results = validator.validate_orders_timestamps(df_orders)
    
    # Missingness correctly tracked
    assert results["missingness"]["order_delivered_customer_date"]["missing"] == 2
    assert results["missingness"]["order_approved_at"]["missing"] == 1
    
    # Status analysis captures expected missingness
    assert results["status_analysis"]["canceled"]["missing_delivery_date"] == 1
    assert results["status_analysis"]["invoiced"]["missing_delivery_date"] == 1

def test_no_data_modification():
    """Validation must not modify input data."""
    validator = TimestampValidator()
    
    df_orders = pd.DataFrame({
        "order_id": ["O1"],
        "order_purchase_timestamp": pd.to_datetime(["2023-01-01 10:00:00"]),
        "order_approved_at": pd.to_datetime([pd.NaT])
    })
    
    df_copy = df_orders.copy()
    validator.validate_orders_timestamps(df_orders)
    
    pd.testing.assert_frame_equal(df_orders, df_copy)
