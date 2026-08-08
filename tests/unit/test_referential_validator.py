import pytest
import pandas as pd
from src.data.referential_validator import ReferentialValidator

def test_perfect_foreign_key_match():
    """Test perfect matching relationships."""
    validator = ReferentialValidator()
    
    df_parent = pd.DataFrame({"p_id": [1, 2, 3]})
    df_child = pd.DataFrame({"c_id": [1, 1, 2, 3]})
    
    res = validator.validate_relationship(df_parent, "p_id", df_child, "c_id")
    
    assert res["matched_rows"] == 4
    assert res["unmatched_rows"] == 0
    assert res["classification"] == "VALID_MATCH"
    assert res["match_percentage"] == 100.0

def test_known_orphan_detection():
    """Test detection of unmatched child keys (orphans)."""
    validator = ReferentialValidator()
    
    df_parent = pd.DataFrame({"p_id": [1, 2]})
    df_child = pd.DataFrame({"c_id": [1, 3]})
    
    res = validator.validate_relationship(df_parent, "p_id", df_child, "c_id")
    
    assert res["matched_rows"] == 1
    assert res["unmatched_rows"] == 1
    assert res["classification"] == "POTENTIAL_ORPHAN"

def test_missing_child_key_handling():
    """Test handling of nulls in the child key column."""
    validator = ReferentialValidator()
    
    df_parent = pd.DataFrame({"p_id": [1, 2]})
    df_child = pd.DataFrame({"c_id": [1, None]})
    
    res = validator.validate_relationship(df_parent, "p_id", df_child, "c_id")
    
    assert res["matched_rows"] == 1
    assert res["missing_child_keys"] == 1
    assert res["unmatched_rows"] == 0
    assert res["classification"] == "MISSING_CHILD_KEY"

def test_translation_table_coverage():
    """Test translation category logic where unmatched is not a true orphan."""
    validator = ReferentialValidator()
    
    df_parent = pd.DataFrame({"cat_pt": ["beleza", "esporte"]})
    df_child = pd.DataFrame({"category": ["beleza", "unknown_cat"]})
    
    res = validator.validate_relationship(df_parent, "cat_pt", df_child, "category", expected_relationship="TRANSLATION")
    
    assert res["matched_rows"] == 1
    assert res["unmatched_rows"] == 1
    assert res["classification"] == "UNTRANSLATED_CATEGORY"

def test_referential_validator_does_not_modify():
    """Ensure dataframes are unmodified."""
    validator = ReferentialValidator()
    
    df_parent = pd.DataFrame({"p_id": [1, 2]})
    df_child = pd.DataFrame({"c_id": [1, 3]})
    
    df_p_copy = df_parent.copy()
    df_c_copy = df_child.copy()
    
    validator.validate_relationship(df_parent, "p_id", df_child, "c_id")
    
    pd.testing.assert_frame_equal(df_parent, df_p_copy)
    pd.testing.assert_frame_equal(df_child, df_c_copy)
