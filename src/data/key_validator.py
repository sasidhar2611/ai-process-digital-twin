import pandas as pd
from typing import Dict, Any, List, Union

class KeyValidator:
    """
    Validates identity and uniqueness characteristics of the Olist datasets.
    Determines if fields are primary keys, expected to repeat, or contain unexpected duplicates.
    DOES NOT modify data.
    """
    
    def validate_key(self, df: pd.DataFrame, key_cols: Union[str, List[str]], expected_uniqueness: str) -> Dict[str, Any]:
        """
        Validates uniqueness or repetition of a key (single or composite).
        expected_uniqueness can be: 'UNIQUE', 'EXPECTED_REPEAT'
        """
        if isinstance(key_cols, str):
            key_cols = [key_cols]
            
        # Ensure columns exist
        missing_cols = [c for c in key_cols if c not in df.columns]
        if missing_cols:
            return {"error": f"Columns missing: {missing_cols}"}
            
        total_rows = len(df)
        
        # Dropna on keys to evaluate uniqueness of actual values
        df_keys = df[key_cols].dropna()
        valid_rows = len(df_keys)
        
        # Calculate counts
        if valid_rows > 0:
            value_counts = df_keys.value_counts()
            unique_count = len(value_counts)
            duplicate_count = valid_rows - unique_count
            max_frequency = int(value_counts.max())
        else:
            unique_count = 0
            duplicate_count = 0
            max_frequency = 0
            
        duplicate_percentage = (duplicate_count / valid_rows * 100) if valid_rows > 0 else 0.0
        
        classification = ""
        if expected_uniqueness == 'UNIQUE':
            if duplicate_count == 0:
                classification = "UNIQUE" if len(key_cols) == 1 else "COMPOSITE_KEY_VALID"
            else:
                classification = "UNEXPECTED_DUPLICATE" if len(key_cols) == 1 else "COMPOSITE_KEY_VIOLATION"
        elif expected_uniqueness == 'EXPECTED_REPEAT':
            classification = "EXPECTED_REPEAT"
            
        return {
            "key": key_cols,
            "expected_uniqueness": expected_uniqueness,
            "total_valid_keys": valid_rows,
            "unique_count": unique_count,
            "duplicate_count": duplicate_count,
            "duplicate_percentage": duplicate_percentage,
            "max_frequency": max_frequency,
            "classification": classification
        }

    def analyze_full_row_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Checks for completely identical rows across all columns.
        """
        total_rows = len(df)
        if total_rows > 0:
            duplicate_rows = int(df.duplicated().sum())
            duplicate_pct = (duplicate_rows / total_rows) * 100
        else:
            duplicate_rows = 0
            duplicate_pct = 0.0
            
        return {
            "total_rows": total_rows,
            "full_row_duplicates": duplicate_rows,
            "duplicate_percentage": duplicate_pct,
            "classification": "FULL_ROW_DUPLICATE" if duplicate_rows > 0 else "NO_DUPLICATE"
        }
