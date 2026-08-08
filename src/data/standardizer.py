import pandas as pd
from typing import Dict, Any

class DataStandardizer:
    """
    Standardizes Olist DataFrames by enforcing column naming conventions (snake_case)
    and converting data to appropriate types (e.g., datetime, string, float).
    Does NOT modify the raw CSV files or perform data cleaning (like filling NaNs).
    """

    # Mapping of original column names to standardized names (fixing typos and ensuring snake_case)
    COLUMN_MAPPINGS = {
        "products": {
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length"
        }
    }

    # Datetime columns per dataset
    DATETIME_COLUMNS = {
        "orders": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],
        "order_items": [
            "shipping_limit_date"
        ],
        "order_reviews": [
            "review_creation_date",
            "review_answer_timestamp"
        ]
    }

    # String (categorical/ID) columns per dataset
    STRING_COLUMNS = {
        "customers": ["customer_id", "customer_unique_id", "customer_city", "customer_state"],
        "geolocation": ["geolocation_city", "geolocation_state"],
        "orders": ["order_id", "customer_id", "order_status"],
        "order_items": ["order_id", "order_item_id", "product_id", "seller_id"],
        "order_payments": ["order_id", "payment_type"],
        "order_reviews": ["review_id", "order_id", "review_comment_title", "review_comment_message"],
        "products": ["product_id", "product_category_name"],
        "sellers": ["seller_id", "seller_city", "seller_state"],
        "product_category_translation": ["product_category_name", "product_category_name_english"]
    }
    
    # Numeric columns per dataset
    NUMERIC_COLUMNS = {
        "order_items": ["price", "freight_value"],
        "order_payments": ["payment_sequential", "payment_installments", "payment_value"],
        "order_reviews": ["review_score"],
        "products": ["product_name_length", "product_description_length", "product_photos_qty", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"],
        "geolocation": ["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"],
        "customers": ["customer_zip_code_prefix"],
        "sellers": ["seller_zip_code_prefix"]
    }

    def standardize_dataset(self, logical_name: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes column names and data types for a specific dataset.
        Returns a new DataFrame to ensure in-memory immutability of the original if passed by reference.
        """
        # Create a copy to avoid SettingWithCopyWarning and preserve original df if needed
        df_std = df.copy()
        
        # 1. Rename columns if necessary
        if logical_name in self.COLUMN_MAPPINGS:
            df_std = df_std.rename(columns=self.COLUMN_MAPPINGS[logical_name])

        # 2. Standardize datetimes
        if logical_name in self.DATETIME_COLUMNS:
            for col in self.DATETIME_COLUMNS[logical_name]:
                if col in df_std.columns:
                    # errors='coerce' to safely parse without dropping rows, just makes invalid ones NaT
                    df_std[col] = pd.to_datetime(df_std[col], errors='coerce')
                    
        # 3. Standardize strings (IDs and Categories)
        if logical_name in self.STRING_COLUMNS:
            for col in self.STRING_COLUMNS[logical_name]:
                if col in df_std.columns:
                    df_std[col] = df_std[col].astype("string")
                    
        # 4. Standardize numerics (use appropriate nullable types like Int64 or Float64 where necessary, 
        #    but standard float64 is fine for now as it supports NaNs). 
        #    We will use float64 for all measurements and prices, and Int64 for integer IDs/quantities to support NaNs.
        if logical_name in self.NUMERIC_COLUMNS:
            for col in self.NUMERIC_COLUMNS[logical_name]:
                if col in df_std.columns:
                    # Basic float conversion to preserve meaning without dropping NaNs
                    df_std[col] = pd.to_numeric(df_std[col], errors='coerce')

        return df_std
