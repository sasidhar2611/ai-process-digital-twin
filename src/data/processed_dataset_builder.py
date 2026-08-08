import pandas as pd
import numpy as np
import os
from typing import Dict, Any

from src.data.raw_data_loader import RawDataLoader
from src.data.standardizer import DataStandardizer
from src.data.validator import TimestampValidator
from src.data.physical_validator import PhysicalValidator

class ProcessedDatasetBuilder:
    """
    Builds analysis-ready processed datasets from raw Olist data.
    Standardizes, validates, and adds explicit derived eligibility flags.
    Saves outputs as parquet.
    """
    
    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = output_dir
        self.loader = RawDataLoader()
        self.standardizer = DataStandardizer()
        self.timestamp_validator = TimestampValidator()
        self.physical_validator = PhysicalValidator()
        
        # Ensure output dir exists
        os.makedirs(self.output_dir, exist_ok=True)
        
    def build_all(self) -> Dict[str, Dict[str, Any]]:
        """Builds all processed datasets and returns quality stats."""
        results = {}
        
        # 1. Orders
        results["processed_orders"] = self._build_orders()
        # 2. Customers
        results["processed_customers"] = self._build_customers()
        # 3. Products
        results["processed_products"] = self._build_products()
        # 4. Items
        results["processed_order_items"] = self._build_order_items()
        # 5. Sellers
        results["processed_sellers"] = self._build_sellers()
        # 6. Payments
        results["processed_payments"] = self._build_payments()
        # 7. Reviews
        results["processed_reviews"] = self._build_reviews()
        
        return results
        
    def _save_and_stat(self, df: pd.DataFrame, source_df: pd.DataFrame, name: str) -> Dict[str, Any]:
        """Saves dataframe and generates quality stats."""
        file_path = os.path.join(self.output_dir, f"{name}.parquet")
        df.to_parquet(file_path, index=False)
        
        return {
            "source_row_count": len(source_df),
            "processed_row_count": len(df),
            "row_difference": len(df) - len(source_df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
        
    def _build_orders(self) -> Dict[str, Any]:
        df_raw = self.loader.load_dataset("orders")
        df = self.standardizer.standardize_dataset("orders", df_raw)
        
        # Eligibility flags
        df["has_approved_timestamp"] = df["order_approved_at"].notna()
        df["eligible_for_demand_timeline"] = df["has_approved_timestamp"]
        
        df["is_delivered_timestamp_complete"] = (
            df["order_delivered_carrier_date"].notna() &
            df["order_delivered_customer_date"].notna()
        )
        
        df["eligible_for_delivery_kpi"] = (
            (df["order_status"] == "delivered") & 
            df["is_delivered_timestamp_complete"]
        )
        
        # Derived fields (Delivery Delay)
        # Delay = delivered customer date - estimated delivery date (in days)
        # Negative means early, positive means late.
        if "order_delivered_customer_date" in df.columns and "order_estimated_delivery_date" in df.columns:
            delay = df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
            df["delivery_delay_days"] = delay.dt.total_seconds() / (24 * 3600)
            
        return self._save_and_stat(df, df_raw, "processed_orders")
        
    def _build_customers(self) -> Dict[str, Any]:
        df_raw = self.loader.load_dataset("customers")
        df = self.standardizer.standardize_dataset("customers", df_raw)
        return self._save_and_stat(df, df_raw, "processed_customers")
        
    def _build_products(self) -> Dict[str, Any]:
        df_raw = self.loader.load_dataset("products")
        df = self.standardizer.standardize_dataset("products", df_raw)
        
        # Flags
        phys_cols = ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]
        df["physical_data_complete"] = df[phys_cols].notna().all(axis=1)
        
        # Validity (must be strictly > 0 for weight, though 0 is present, we flag it)
        # For dimensions > 0
        df["physical_measurement_valid"] = (
            df["physical_data_complete"] &
            (df["product_weight_g"] > 0) &
            (df["product_length_cm"] > 0) &
            (df["product_height_cm"] > 0) &
            (df["product_width_cm"] > 0)
        )
        
        # Derived Volume
        df["physical_volume_cm3"] = self.physical_validator.derive_volume(df)
        
        return self._save_and_stat(df, df_raw, "processed_products")
        
    def _build_order_items(self) -> Dict[str, Any]:
        df_raw = self.loader.load_dataset("order_items")
        df = self.standardizer.standardize_dataset("order_items", df_raw)
        return self._save_and_stat(df, df_raw, "processed_order_items")
        
    def _build_sellers(self) -> Dict[str, Any]:
        df_raw = self.loader.load_dataset("sellers")
        df = self.standardizer.standardize_dataset("sellers", df_raw)
        return self._save_and_stat(df, df_raw, "processed_sellers")
        
    def _build_payments(self) -> Dict[str, Any]:
        df_raw = self.loader.load_dataset("order_payments")
        df = self.standardizer.standardize_dataset("order_payments", df_raw)
        return self._save_and_stat(df, df_raw, "processed_payments")
        
    def _build_reviews(self) -> Dict[str, Any]:
        df_raw = self.loader.load_dataset("order_reviews")
        df = self.standardizer.standardize_dataset("order_reviews", df_raw)
        return self._save_and_stat(df, df_raw, "processed_reviews")
