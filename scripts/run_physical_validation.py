import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.raw_data_loader import RawDataLoader
from src.data.physical_validator import PhysicalValidator

def run_physical_validation():
    loader = RawDataLoader()
    validator = PhysicalValidator()
    
    print("Loading datasets...")
    df_products = loader.load_dataset("products")
    
    physical_fields = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]
    
    print("Analyzing completeness...")
    completeness = validator.analyze_completeness(df_products, physical_fields)
    
    print("Validating physical fields...")
    field_stats = validator.validate_physical_fields(df_products, physical_fields)
    
    print("Deriving volume...")
    volume = validator.derive_volume(df_products)
    
    # Calculate volume stats separately since it's derived
    volume_numeric = pd.to_numeric(volume, errors="coerce")
    volume_missing = int(volume_numeric.isna().sum())
    volume_valid = volume_numeric.dropna()
    
    volume_stats = {
        "count": len(volume_numeric),
        "missing_count": volume_missing,
        "missing_percentage": (volume_missing / len(volume_numeric) * 100) if len(volume_numeric) > 0 else 0.0
    }
    
    if len(volume_valid) > 0:
        zero_count = int((volume_valid == 0).sum())
        negative_count = int((volume_valid < 0).sum())
        
        volume_stats.update({
            "min": float(volume_valid.min()),
            "max": float(volume_valid.max()),
            "mean": float(volume_valid.mean()),
            "median": float(volume_valid.median()),
            "p01": float(volume_valid.quantile(0.01)),
            "p05": float(volume_valid.quantile(0.05)),
            "p25": float(volume_valid.quantile(0.25)),
            "p50": float(volume_valid.quantile(0.50)),
            "p75": float(volume_valid.quantile(0.75)),
            "p95": float(volume_valid.quantile(0.95)),
            "p99": float(volume_valid.quantile(0.99)),
            "zero_count": zero_count,
            "negative_count": negative_count
        })
        
        q1 = volume_valid.quantile(0.25)
        q3 = volume_valid.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = volume_valid[(volume_valid < lower_bound) | (volume_valid > upper_bound)]
        volume_stats["outlier_count"] = int(len(outliers))
        
    results = {
        "completeness": completeness,
        "fields": field_stats,
        "derived_volume": volume_stats
    }
    
    with open("product_physical_validation_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
if __name__ == "__main__":
    import pandas as pd
    run_physical_validation()
