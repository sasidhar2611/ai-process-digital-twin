import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.raw_data_loader import RawDataLoader
from src.data.standardizer import DataStandardizer
from src.data.validator import TimestampValidator

def run_validation():
    print("Loading data...")
    loader = RawDataLoader()
    df_orders_raw = loader.load_dataset("orders")
    df_items_raw = loader.load_dataset("order_items")
    
    print("Standardizing data...")
    std = DataStandardizer()
    df_orders = std.standardize_dataset("orders", df_orders_raw)
    df_items = std.standardize_dataset("order_items", df_items_raw)
    
    print("Validating data...")
    validator = TimestampValidator()
    results_orders = validator.validate_orders_timestamps(df_orders)
    results_items = validator.validate_order_items_timestamps(df_items, df_orders)
    
    print("\n--- ORDERS RESULTS ---")
    print(json.dumps(results_orders, indent=2))
    
    print("\n--- ITEMS RESULTS ---")
    print(json.dumps(results_items, indent=2))
    
    with open("validation_results.json", "w") as f:
        json.dump({"orders": results_orders, "items": results_items}, f, indent=2)
        
if __name__ == "__main__":
    run_validation()
