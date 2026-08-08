import pandas as pd
import numpy as np
from typing import Dict, Any, List

class PhysicalValidator:
    """
    Validates physical product attributes (weight, length, height, width).
    Calculates completeness, validity (zeros/negatives), statistics, and outliers.
    """
    
    def validate_physical_fields(self, df: pd.DataFrame, fields: List[str]) -> Dict[str, Any]:
        """
        Validates basic stats for each physical field.
        """
        results = {}
        for field in fields:
            if field not in df.columns:
                results[field] = {"error": "Field not found"}
                continue
                
            s = df[field]
            s_numeric = pd.to_numeric(s, errors="coerce")
            
            missing_count = int(s_numeric.isna().sum())
            total_count = len(s_numeric)
            valid_count = total_count - missing_count
            
            stats = {
                "count": total_count,
                "missing_count": missing_count,
                "missing_percentage": (missing_count / total_count * 100) if total_count > 0 else 0.0,
            }
            
            if valid_count > 0:
                s_valid = s_numeric.dropna()
                
                # Validity
                zero_count = int((s_valid == 0).sum())
                negative_count = int((s_valid < 0).sum())
                
                # Stats
                stats.update({
                    "min": float(s_valid.min()),
                    "max": float(s_valid.max()),
                    "mean": float(s_valid.mean()),
                    "median": float(s_valid.median()),
                    "std": float(s_valid.std()) if valid_count > 1 else 0.0,
                    "p01": float(s_valid.quantile(0.01)),
                    "p05": float(s_valid.quantile(0.05)),
                    "p25": float(s_valid.quantile(0.25)),
                    "p50": float(s_valid.quantile(0.50)),
                    "p75": float(s_valid.quantile(0.75)),
                    "p95": float(s_valid.quantile(0.95)),
                    "p99": float(s_valid.quantile(0.99)),
                    "zero_count": zero_count,
                    "negative_count": negative_count
                })
                
                # Outliers using IQR (Q3 + 1.5*IQR)
                q1 = s_valid.quantile(0.25)
                q3 = s_valid.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                outliers = s_valid[(s_valid < lower_bound) | (s_valid > upper_bound)]
                stats["outlier_count"] = int(len(outliers))
                stats["iqr_lower_bound"] = float(lower_bound)
                stats["iqr_upper_bound"] = float(upper_bound)
                
            results[field] = stats
            
        return results

    def analyze_completeness(self, df: pd.DataFrame, fields: List[str]) -> Dict[str, Any]:
        """
        Analyzes row-level completeness for the specified fields.
        """
        if not fields:
            return {"error": "No fields specified"}
            
        # Ensure all fields exist
        existing_fields = [f for f in fields if f in df.columns]
        
        if not existing_fields:
            return {"error": "None of the fields exist"}
            
        # Count rows where ALL fields are not null
        complete_mask = df[existing_fields].notna().all(axis=1)
        complete_count = int(complete_mask.sum())
        total_count = len(df)
        incomplete_count = total_count - complete_count
        
        return {
            "total_products": total_count,
            "complete_physical_records": complete_count,
            "incomplete_physical_records": incomplete_count,
            "completeness_percentage": (complete_count / total_count * 100) if total_count > 0 else 0.0
        }
        
    def derive_volume(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Derives product volume (cm3) from dimensions without mutating original dataframe.
        """
        # We work on a copy to ensure we don't modify raw data inplace unexpectedly,
        # but normally derived fields are just returned or added to a new dataframe.
        # To strictly adhere to "DO NOT write it into the raw dataset", we'll just return a Series.
        
        dims = ["product_length_cm", "product_height_cm", "product_width_cm"]
        if not all(col in df.columns for col in dims):
            return pd.Series(index=df.index, dtype=float)
            
        # Calculate volume
        volume = df["product_length_cm"] * df["product_height_cm"] * df["product_width_cm"]
        return volume
