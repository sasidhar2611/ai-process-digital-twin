import pytest
import pandas as pd
import numpy as np
import tempfile
import hashlib
from pathlib import Path
from src.data.standardizer import DataStandardizer
from src.data.raw_data_loader import RawDataLoader

def test_column_naming_standardization():
    """Test that columns with typos (e.g., product_name_lenght) are standardized."""
    std = DataStandardizer()
    df_raw = pd.DataFrame({
        "product_id": ["P1"], 
        "product_name_lenght": [50], 
        "product_description_lenght": [500]
    })
    
    df_std = std.standardize_dataset("products", df_raw)
    
    assert "product_name_length" in df_std.columns
    assert "product_description_length" in df_std.columns
    assert "product_name_lenght" not in df_std.columns

def test_data_type_standardization_datetime():
    """Test that timestamp fields become datetime objects."""
    std = DataStandardizer()
    df_raw = pd.DataFrame({
        "order_id": ["O1", "O2"],
        "order_purchase_timestamp": ["2023-01-01 10:00:00", "invalid_date"]
    })
    
    df_std = std.standardize_dataset("orders", df_raw)
    
    # Check type is datetime
    assert pd.api.types.is_datetime64_any_dtype(df_std["order_purchase_timestamp"])
    
    # Check that invalid dates become NaT instead of raising or dropping row
    assert not pd.isna(df_std["order_purchase_timestamp"].iloc[0])
    assert pd.isna(df_std["order_purchase_timestamp"].iloc[1])
    assert len(df_std) == 2  # Row count unchanged

def test_data_type_standardization_string():
    """Test that string categorical fields are standardized as string dtype."""
    std = DataStandardizer()
    df_raw = pd.DataFrame({
        "customer_id": [123, 456], # Integers simulating raw parsing
        "customer_state": ["SP", "RJ"]
    })
    
    df_std = std.standardize_dataset("customers", df_raw)
    assert pd.api.types.is_string_dtype(df_std["customer_id"])
    assert pd.api.types.is_string_dtype(df_std["customer_state"])
    assert df_std["customer_id"].iloc[0] == "123"

def test_data_type_standardization_numeric():
    """Test numeric standardizations handle numeric values correctly without dropping NaN."""
    std = DataStandardizer()
    df_raw = pd.DataFrame({
        "order_id": ["O1", "O2"],
        "price": ["10.5", "invalid"]
    })
    
    df_std = std.standardize_dataset("order_items", df_raw)
    assert pd.api.types.is_numeric_dtype(df_std["price"])
    assert df_std["price"].iloc[0] == 10.5
    assert pd.isna(df_std["price"].iloc[1])

def test_no_row_dropping():
    """Standardization must not alter row counts."""
    std = DataStandardizer()
    df_raw = pd.DataFrame({
        "product_id": ["P1", "P2", "P3"],
        "product_weight_g": [100, None, 200]
    })
    
    df_std = std.standardize_dataset("products", df_raw)
    assert len(df_std) == 3

def test_raw_data_immutability(tmp_path):
    """Ensure that standardizer along with loader does not modify the raw CSV files."""
    file_path = tmp_path / "olist_products_dataset.csv"
    df_mock = pd.DataFrame({
        "product_id": ["P1"], 
        "product_name_lenght": [50]
    })
    df_mock.to_csv(file_path, index=False)
    
    # Record state before
    stat_before = file_path.stat()
    with open(file_path, "rb") as f:
        hash_before = hashlib.md5(f.read()).hexdigest()
        
    # Load and standardize
    loader = RawDataLoader(data_dir=str(tmp_path))
    df_raw = loader.load_dataset("products")
    
    std = DataStandardizer()
    df_std = std.standardize_dataset("products", df_raw)
    
    # Verify standardizer worked
    assert "product_name_length" in df_std.columns
    
    # Record state after
    stat_after = file_path.stat()
    with open(file_path, "rb") as f:
        hash_after = hashlib.md5(f.read()).hexdigest()
        
    assert stat_before.st_size == stat_after.st_size
    assert stat_before.st_mtime == stat_after.st_mtime
    assert hash_before == hash_after
