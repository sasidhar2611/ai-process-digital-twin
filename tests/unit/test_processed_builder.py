import pytest
import pandas as pd
import os
import shutil
from src.data.processed_dataset_builder import ProcessedDatasetBuilder

def test_processed_dataset_builder(tmp_path):
    """Test building processed datasets."""
    # Use temporary directory for testing
    builder = ProcessedDatasetBuilder(output_dir=str(tmp_path))
    
    results = builder.build_all()
    
    # 1. Output datasets exist
    expected_files = [
        "processed_orders.parquet",
        "processed_customers.parquet",
        "processed_products.parquet",
        "processed_order_items.parquet",
        "processed_sellers.parquet",
        "processed_payments.parquet",
        "processed_reviews.parquet"
    ]
    
    for filename in expected_files:
        assert os.path.exists(os.path.join(tmp_path, filename))
        
    # 2. Results format
    assert "processed_orders" in results
    assert "source_row_count" in results["processed_orders"]
    assert "processed_row_count" in results["processed_orders"]
    assert results["processed_orders"]["row_difference"] == 0
    
    # 3. Flags exist in orders
    order_cols = results["processed_orders"]["columns"]
    assert "has_approved_timestamp" in order_cols
    assert "eligible_for_demand_timeline" in order_cols
    assert "eligible_for_delivery_kpi" in order_cols
    
    # 4. Flags exist in products
    product_cols = results["processed_products"]["columns"]
    assert "physical_data_complete" in product_cols
    assert "physical_measurement_valid" in product_cols
    assert "physical_volume_cm3" in product_cols
    
    # 5. Row retention
    assert results["processed_orders"]["processed_row_count"] > 0
    
def test_processing_is_deterministic(tmp_path):
    builder1 = ProcessedDatasetBuilder(output_dir=os.path.join(tmp_path, "run1"))
    builder2 = ProcessedDatasetBuilder(output_dir=os.path.join(tmp_path, "run2"))
    
    res1 = builder1.build_all()
    res2 = builder2.build_all()
    
    assert res1["processed_orders"]["processed_row_count"] == res2["processed_orders"]["processed_row_count"]
    
    # Check physical content
    df1 = pd.read_parquet(os.path.join(tmp_path, "run1", "processed_orders.parquet"))
    df2 = pd.read_parquet(os.path.join(tmp_path, "run2", "processed_orders.parquet"))
    
    pd.testing.assert_frame_equal(df1, df2)
