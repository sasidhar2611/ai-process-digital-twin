import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.raw_data_loader import RawDataLoader
from src.data.standardizer import DataStandardizer
from src.data.missing_handler import MissingValueHandler

def run_missing_analysis():
    loader = RawDataLoader()
    std = DataStandardizer()
    handler = MissingValueHandler()
    
    datasets = ["orders", "order_items", "products", "customers", "sellers", "order_payments", "order_reviews"]
    
    final_results = {}
    
    for d in datasets:
        print(f"Analyzing {d}...")
        df_raw = loader.load_dataset(d)
        df_std = std.standardize_dataset(d, df_raw)
        res = handler.analyze_missingness(df_std, d)
        
        # Only keep fields that actually have missing values or are explicitly classified
        missing_fields = {}
        for col, info in res["fields"].items():
            if info["missing_count"] > 0 or info.get("classification"):
                missing_fields[col] = info
                
        final_results[d] = {
            "total_records": res["total_records"],
            "missing_fields": missing_fields
        }
        
    with open("missing_analysis_results.json", "w") as f:
        json.dump(final_results, f, indent=2)
        
if __name__ == "__main__":
    run_missing_analysis()
