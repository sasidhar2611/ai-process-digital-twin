import pytest
import pandas as pd
from src.data.key_validator import KeyValidator

def test_unique_key_validation():
    """Test detection of unique key valid and violation cases."""
    validator = KeyValidator()
    
    # Valid unique key
    df_valid = pd.DataFrame({"id": [1, 2, 3], "val": ["A", "B", "C"]})
    res_valid = validator.validate_key(df_valid, "id", "UNIQUE")
    assert res_valid["classification"] == "UNIQUE"
    assert res_valid["duplicate_count"] == 0
    
    # Invalid unique key
    df_invalid = pd.DataFrame({"id": [1, 1, 3], "val": ["A", "B", "C"]})
    res_invalid = validator.validate_key(df_invalid, "id", "UNIQUE")
    assert res_invalid["classification"] == "UNEXPECTED_DUPLICATE"
    assert res_invalid["duplicate_count"] == 1
    assert res_invalid["max_frequency"] == 2

def test_composite_key_validation():
    """Test composite key valid and violation cases."""
    validator = KeyValidator()
    
    # Valid composite key
    df_comp = pd.DataFrame({"order_id": [1, 1, 2], "item_id": [1, 2, 1], "val": ["A", "B", "C"]})
    res_valid = validator.validate_key(df_comp, ["order_id", "item_id"], "UNIQUE")
    assert res_valid["classification"] == "COMPOSITE_KEY_VALID"
    assert res_valid["duplicate_count"] == 0
    
    # Invalid composite key
    df_comp_invalid = pd.DataFrame({"order_id": [1, 1, 2], "item_id": [1, 1, 1], "val": ["A", "B", "C"]})
    res_invalid = validator.validate_key(df_comp_invalid, ["order_id", "item_id"], "UNIQUE")
    assert res_invalid["classification"] == "COMPOSITE_KEY_VIOLATION"
    assert res_invalid["duplicate_count"] == 1
    assert res_invalid["max_frequency"] == 2

def test_expected_repeat_key():
    """Test expected repeating key detection."""
    validator = KeyValidator()
    df = pd.DataFrame({"zip": ["123", "123", "456"]})
    res = validator.validate_key(df, "zip", "EXPECTED_REPEAT")
    
    assert res["classification"] == "EXPECTED_REPEAT"
    assert res["duplicate_count"] == 1

def test_full_row_duplicates():
    """Test full duplicate row detection."""
    validator = KeyValidator()
    
    # No duplicate rows
    df_clean = pd.DataFrame({"id": [1, 2], "val": ["A", "B"]})
    res_clean = validator.analyze_full_row_duplicates(df_clean)
    assert res_clean["classification"] == "NO_DUPLICATE"
    assert res_clean["full_row_duplicates"] == 0
    
    # Duplicate rows
    df_dup = pd.DataFrame({"id": [1, 1, 2], "val": ["A", "A", "B"]})
    res_dup = validator.analyze_full_row_duplicates(df_dup)
    assert res_dup["classification"] == "FULL_ROW_DUPLICATE"
    assert res_dup["full_row_duplicates"] == 1

def test_no_data_modification():
    """Ensure validation does not alter input data."""
    validator = KeyValidator()
    df = pd.DataFrame({"id": [1, 1], "val": ["A", "A"]})
    df_copy = df.copy()
    
    validator.validate_key(df, "id", "UNIQUE")
    validator.analyze_full_row_duplicates(df)
    
    pd.testing.assert_frame_equal(df, df_copy)
