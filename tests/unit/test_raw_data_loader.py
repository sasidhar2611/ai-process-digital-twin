import os
import tempfile
import pytest
import pandas as pd
from pathlib import Path
from src.data.raw_data_loader import RawDataLoader
import hashlib

@pytest.fixture
def temp_data_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create a dummy olist_customers_dataset.csv
        file_path = Path(tmpdirname) / "olist_customers_dataset.csv"
        df = pd.DataFrame({"customer_id": ["A", "B"], "customer_city": ["Sao Paulo", "Rio"]})
        df.to_csv(file_path, index=False)
        yield tmpdirname

def test_loader_custom_dir(temp_data_dir):
    loader = RawDataLoader(data_dir=temp_data_dir)
    assert loader.validate_directory() is True
    
    presence = loader.validate_expected_files()
    assert presence["customers"] is True
    assert presence["orders"] is False

def test_load_dataset_success(temp_data_dir):
    loader = RawDataLoader(data_dir=temp_data_dir)
    df = loader.load_dataset("customers")
    assert not df.empty
    assert list(df.columns) == ["customer_id", "customer_city"]
    assert len(df) == 2

def test_load_dataset_invalid_name(temp_data_dir):
    loader = RawDataLoader(data_dir=temp_data_dir)
    with pytest.raises(ValueError):
        loader.load_dataset("non_existent_logical_name")

def test_load_dataset_file_not_found(temp_data_dir):
    loader = RawDataLoader(data_dir=temp_data_dir)
    with pytest.raises(FileNotFoundError):
        loader.load_dataset("orders")

def test_real_raw_data_immutability():
    """
    Test that loading the real dataset does not modify the underlying files.
    This fulfills the strictly enforced immutability requirement.
    """
    loader = RawDataLoader()
    if not loader.validate_directory():
        pytest.skip("Real raw data directory not found, skipping immutability test.")
    
    presence = loader.validate_expected_files()
    if not presence["customers"]:
        pytest.skip("customers dataset missing in real raw data, skipping immutability test.")
        
    file_path = loader.data_dir / "olist_customers_dataset.csv"
    
    # Capture state before loading
    stat_before = file_path.stat()
    with open(file_path, "rb") as f:
        hash_before = hashlib.md5(f.read()).hexdigest()
        
    # Load dataset
    df = loader.load_dataset("customers")
    
    # Capture state after loading
    stat_after = file_path.stat()
    with open(file_path, "rb") as f:
        hash_after = hashlib.md5(f.read()).hexdigest()
        
    # Assertions
    assert stat_before.st_size == stat_after.st_size, "File size was modified!"
    assert stat_before.st_mtime == stat_after.st_mtime, "File modification time was altered!"
    assert hash_before == hash_after, "File contents were modified!"
    
    # Verify we got a reasonable DataFrame
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
