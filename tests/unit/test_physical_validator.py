import pytest
import pandas as pd
import numpy as np
from src.data.physical_validator import PhysicalValidator

def test_derived_volume():
    """Test correct volume calculation."""
    validator = PhysicalValidator()
    
    df = pd.DataFrame({
        "product_length_cm": [10.0, 5.0, np.nan],
        "product_height_cm": [10.0, 2.0, 10.0],
        "product_width_cm": [10.0, 3.0, 10.0]
    })
    
    volume = validator.derive_volume(df)
    
    assert len(volume) == 3
    assert volume[0] == 1000.0
    assert volume[1] == 30.0
    assert np.isnan(volume[2])

def test_missing_data_detection():
    """Test missing physical data detection."""
    validator = PhysicalValidator()
    
    df = pd.DataFrame({
        "product_weight_g": [100.0, np.nan, 200.0],
        "product_length_cm": [10.0, 10.0, np.nan]
    })
    
    res = validator.analyze_completeness(df, ["product_weight_g", "product_length_cm"])
    
    assert res["total_products"] == 3
    assert res["complete_physical_records"] == 1
    assert res["incomplete_physical_records"] == 2
    assert res["completeness_percentage"] == pytest.approx(33.33, 0.1)

def test_zero_and_negative_detection():
    """Test zero and negative value detection."""
    validator = PhysicalValidator()
    
    df = pd.DataFrame({
        "product_weight_g": [100.0, 0.0, -50.0, np.nan]
    })
    
    res = validator.validate_physical_fields(df, ["product_weight_g"])
    
    assert res["product_weight_g"]["zero_count"] == 1
    assert res["product_weight_g"]["negative_count"] == 1
    assert res["product_weight_g"]["missing_count"] == 1

def test_outlier_detection():
    """Test IQR outlier detection."""
    validator = PhysicalValidator()
    
    # 1, 2, 3, 4, 5, 100 (100 is outlier)
    df = pd.DataFrame({
        "product_weight_g": [1.0, 2.0, 3.0, 4.0, 5.0, 100.0]
    })
    
    res = validator.validate_physical_fields(df, ["product_weight_g"])
    
    # IQR is 4.75 - 2.25 = 2.5
    # Upper bound = 4.75 + 1.5*2.5 = 8.5
    assert res["product_weight_g"]["outlier_count"] == 1
    assert res["product_weight_g"]["max"] == 100.0

def test_validator_does_not_modify_input():
    """Ensure dataframes are unmodified."""
    validator = PhysicalValidator()
    
    df = pd.DataFrame({
        "product_length_cm": [10.0, 20.0],
        "product_height_cm": [10.0, 20.0],
        "product_width_cm": [10.0, 20.0]
    })
    
    df_copy = df.copy()
    
    validator.derive_volume(df)
    validator.analyze_completeness(df, ["product_length_cm"])
    validator.validate_physical_fields(df, ["product_length_cm"])
    
    pd.testing.assert_frame_equal(df, df_copy)
