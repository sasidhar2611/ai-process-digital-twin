import pandas as pd
from typing import Dict, Any

class ReferentialValidator:
    """
    Validates referential integrity between parent and child datasets.
    Identifies matched rows, orphans, and categorizes failures explicitly.
    DOES NOT modify data.
    """
    
    def validate_relationship(
        self,
        df_parent: pd.DataFrame,
        parent_key: str,
        df_child: pd.DataFrame,
        child_key: str,
        expected_relationship: str = "FOREIGN_KEY"
    ) -> Dict[str, Any]:
        """
        Validates the mapping of child_key values to parent_key values.
        expected_relationship could be 'FOREIGN_KEY' or 'TRANSLATION' to adjust classification rules.
        """
        if parent_key not in df_parent.columns or child_key not in df_child.columns:
            return {"error": f"Key columns not found. Parent: {parent_key}, Child: {child_key}"}
            
        child_rows = len(df_child)
        
        # Filter out nulls in child key - missing child key is a different issue
        child_valid_keys = df_child[df_child[child_key].notna()][child_key]
        missing_child_keys = child_rows - len(child_valid_keys)
        
        parent_unique_keys = set(df_parent[parent_key].dropna().unique())
        
        matched_mask = child_valid_keys.isin(parent_unique_keys)
        matched_rows = int(matched_mask.sum())
        unmatched_rows = len(child_valid_keys) - matched_rows
        
        match_percentage = (matched_rows / child_rows * 100) if child_rows > 0 else 0.0
        orphan_percentage = (unmatched_rows / child_rows * 100) if child_rows > 0 else 0.0
        
        classification = "VALID_MATCH"
        
        if unmatched_rows > 0:
            if expected_relationship == "TRANSLATION":
                classification = "UNTRANSLATED_CATEGORY"
            else:
                classification = "POTENTIAL_ORPHAN"
                
        # If missing keys exist in child, record it
        if missing_child_keys > 0 and classification == "VALID_MATCH":
            classification = "MISSING_CHILD_KEY"

        return {
            "parent_key": parent_key,
            "child_key": child_key,
            "child_rows": child_rows,
            "matched_rows": matched_rows,
            "unmatched_rows": unmatched_rows,
            "missing_child_keys": missing_child_keys,
            "match_percentage": match_percentage,
            "orphan_percentage": orphan_percentage,
            "classification": classification,
            "expected_relationship": expected_relationship
        }
