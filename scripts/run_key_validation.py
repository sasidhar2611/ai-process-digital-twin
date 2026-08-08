import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.raw_data_loader import RawDataLoader
from src.data.key_validator import KeyValidator

def run_key_validation():
    loader = RawDataLoader()
    validator = KeyValidator()
    
    datasets_to_check = {
        "customers": [
            ("customer_id", "UNIQUE"),
            ("customer_unique_id", "EXPECTED_REPEAT")
        ],
        "orders": [
            ("order_id", "UNIQUE"),
            ("customer_id", "EXPECTED_REPEAT")
        ],
        "order_items": [
            (["order_id", "order_item_id"], "UNIQUE"),
            ("order_id", "EXPECTED_REPEAT")
        ],
        "products": [
            ("product_id", "UNIQUE")
        ],
        "sellers": [
            ("seller_id", "UNIQUE")
        ],
        "order_payments": [
            (["order_id", "payment_sequential"], "UNIQUE"),
            ("order_id", "EXPECTED_REPEAT")
        ],
        "order_reviews": [
            ("review_id", "UNIQUE"),
            ("order_id", "EXPECTED_REPEAT")
        ],
        "geolocation": [
            ("geolocation_zip_code_prefix", "EXPECTED_REPEAT")
        ],
        "product_category_translation": [
            ("product_category_name", "UNIQUE")
        ]
    }
    
    results = {}
    
    for dataset_name, keys_to_check in datasets_to_check.items():
        print(f"Analyzing {dataset_name}...")
        df = loader.load_dataset(dataset_name)
        
        dataset_results = {
            "full_row_duplicates": validator.analyze_full_row_duplicates(df),
            "key_validations": []
        }
        
        for key_def, expected in keys_to_check:
            res = validator.validate_key(df, key_def, expected)
            dataset_results["key_validations"].append(res)
            
        # Specific order items logic
        if dataset_name == "order_items":
            dataset_results["custom_analysis"] = {
                "unique_orders": int(df["order_id"].nunique()),
                "total_items": len(df),
                "max_item_id_overall": int(df["order_item_id"].max()),
                "min_item_id_overall": int(df["order_item_id"].min())
            }
            
        results[dataset_name] = dataset_results
        
    with open("key_validation_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
if __name__ == "__main__":
    run_key_validation()
