import pytest
import pandas as pd
from src.data.missing_handler import MissingValueHandler

def test_missingness_analysis_orders():
    """Test analysis correctly identifies expected missing vs issues for orders."""
    handler = MissingValueHandler()
    
    df_orders = pd.DataFrame({
        "order_id": ["O1", "O2", "O3", "O4"],
        "order_status": ["delivered", "canceled", "shipped", "delivered"],
        "order_approved_at": pd.to_datetime(["2023-01-01", "2023-01-02", pd.NaT, "2023-01-04"]),
        "order_delivered_carrier_date": pd.to_datetime(["2023-01-02", pd.NaT, "2023-01-04", pd.NaT]),
        "order_delivered_customer_date": pd.to_datetime(["2023-01-05", pd.NaT, pd.NaT, pd.NaT])
    })
    
    res = handler.analyze_missingness(df_orders, "orders")
    
    # 1. Delivered customer date
    cust_date = res["fields"]["order_delivered_customer_date"]
    assert cust_date["missing_count"] == 3
    assert cust_date["classification"]["EXPECTED_MISSING"] == 2 # canceled, shipped
    assert cust_date["classification"]["POTENTIAL_DATA_QUALITY_ISSUE"] == 1 # delivered
    
    # 2. Approved at
    app_date = res["fields"]["order_approved_at"]
    assert app_date["missing_count"] == 1
    assert app_date["classification"]["EXPECTED_MISSING"] == 0
    assert app_date["classification"]["POTENTIAL_DATA_QUALITY_ISSUE"] == 1
    
def test_missingness_analysis_products():
    """Test analysis for product dimensions."""
    handler = MissingValueHandler()
    
    df_products = pd.DataFrame({
        "product_id": ["P1", "P2"],
        "product_weight_g": [100.0, pd.NA]
    })
    
    res = handler.analyze_missingness(df_products, "products")
    weight_res = res["fields"]["product_weight_g"]
    
    assert weight_res["missing_count"] == 1
    assert weight_res["classification"]["POTENTIAL_DATA_QUALITY_ISSUE"] == 1

def test_apply_treatment_retains_nulls():
    """Ensure treatment correctly applies RETAIN_AS_NULL without dropping or imputing."""
    handler = MissingValueHandler()
    
    df_orders = pd.DataFrame({
        "order_id": ["O1", "O2"],
        "order_approved_at": pd.to_datetime(["2023-01-01", pd.NaT])
    })
    
    df_copy = df_orders.copy()
    
    df_treated = handler.apply_treatment(df_orders, "orders")
    
    # Raw dataframe must be unchanged
    pd.testing.assert_frame_equal(df_orders, df_copy)
    
    # Treated dataframe must retain the NULLs
    assert df_treated["order_approved_at"].isna().sum() == 1
    
    # Check policy mapping
    assert handler.treatment_policies["order_approved_at"] == "RETAIN_AS_NULL"
