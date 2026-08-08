import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.raw_data_loader import RawDataLoader
from src.data.referential_validator import ReferentialValidator

def run_referential_validation():
    loader = RawDataLoader()
    validator = ReferentialValidator()
    
    print("Loading datasets...")
    df_orders = loader.load_dataset("orders")
    df_customers = loader.load_dataset("customers")
    df_items = loader.load_dataset("order_items")
    df_products = loader.load_dataset("products")
    df_sellers = loader.load_dataset("sellers")
    df_payments = loader.load_dataset("order_payments")
    df_reviews = loader.load_dataset("order_reviews")
    df_translation = loader.load_dataset("product_category_translation")
    
    relationships_to_test = [
        {
            "name": "orders_to_customers",
            "parent_df": df_customers, "parent_key": "customer_id",
            "child_df": df_orders, "child_key": "customer_id",
            "type": "FOREIGN_KEY"
        },
        {
            "name": "items_to_orders",
            "parent_df": df_orders, "parent_key": "order_id",
            "child_df": df_items, "child_key": "order_id",
            "type": "FOREIGN_KEY"
        },
        {
            "name": "items_to_products",
            "parent_df": df_products, "parent_key": "product_id",
            "child_df": df_items, "child_key": "product_id",
            "type": "FOREIGN_KEY"
        },
        {
            "name": "items_to_sellers",
            "parent_df": df_sellers, "parent_key": "seller_id",
            "child_df": df_items, "child_key": "seller_id",
            "type": "FOREIGN_KEY"
        },
        {
            "name": "payments_to_orders",
            "parent_df": df_orders, "parent_key": "order_id",
            "child_df": df_payments, "child_key": "order_id",
            "type": "FOREIGN_KEY"
        },
        {
            "name": "reviews_to_orders",
            "parent_df": df_orders, "parent_key": "order_id",
            "child_df": df_reviews, "child_key": "order_id",
            "type": "FOREIGN_KEY"
        },
        {
            "name": "products_to_translation",
            "parent_df": df_translation, "parent_key": "product_category_name",
            "child_df": df_products, "child_key": "product_category_name",
            "type": "TRANSLATION"
        }
    ]
    
    results = {}
    
    for rel in relationships_to_test:
        print(f"Validating {rel['name']}...")
        res = validator.validate_relationship(
            rel["parent_df"], rel["parent_key"],
            rel["child_df"], rel["child_key"],
            rel["type"]
        )
        results[rel["name"]] = res
        
    # Custom review analysis
    print("Performing custom review analysis...")
    reviews_per_order = df_reviews.groupby("order_id")["review_id"].count()
    orders_per_review = df_reviews.groupby("review_id")["order_id"].count()
    
    results["custom_review_analysis"] = {
        "max_reviews_per_order": int(reviews_per_order.max()),
        "orders_with_multiple_reviews": int((reviews_per_order > 1).sum()),
        "max_orders_per_review": int(orders_per_review.max()),
        "reviews_mapping_to_multiple_orders": int((orders_per_review > 1).sum())
    }
    
    # Custom order items analysis
    print("Performing custom items analysis...")
    items_per_order = df_items.groupby("order_id")["order_item_id"].count()
    results["custom_items_analysis"] = {
        "min_items_per_order": int(items_per_order.min()),
        "max_items_per_order": int(items_per_order.max())
    }

    with open("referential_integrity_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
if __name__ == "__main__":
    run_referential_validation()
