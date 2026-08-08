import pandas as pd
from typing import Dict, Any

class MissingValueHandler:
    """
    Analyzes and handles missing values in Olist datasets.
    Distinguishes between EXPECTED_MISSING and POTENTIAL_DATA_QUALITY_ISSUE.
    Applies explicit treatment policies (mostly RETAIN_AS_NULL per business rules).
    """

    def __init__(self):
        # Define treatment policies
        self.treatment_policies = {
            "order_purchase_timestamp": "RETAIN_AS_NULL",
            "order_approved_at": "RETAIN_AS_NULL",
            "order_delivered_carrier_date": "RETAIN_AS_NULL",
            "order_delivered_customer_date": "RETAIN_AS_NULL",
            "order_estimated_delivery_date": "RETAIN_AS_NULL",
            "product_weight_g": "RETAIN_AS_NULL",
            "product_length_cm": "RETAIN_AS_NULL",
            "product_height_cm": "RETAIN_AS_NULL",
            "product_width_cm": "RETAIN_AS_NULL"
        }

    def analyze_missingness(self, df: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        """
        Analyzes a standardized dataframe and returns structured missingness statistics and classifications.
        """
        results = {
            "dataset": dataset_name,
            "total_records": len(df),
            "fields": {}
        }
        
        for col in df.columns:
            missing_count = int(df[col].isna().sum())
            missing_pct = (missing_count / len(df)) * 100 if len(df) > 0 else 0.0
            
            field_analysis = {
                "missing_count": missing_count,
                "missing_percentage": missing_pct,
                "data_type": str(df[col].dtype),
                "classification": {},
                "treatment": self.treatment_policies.get(col, "RETAIN_AS_NULL")
            }
            
            # Specific domain rules for classification
            if dataset_name == "orders":
                if col == "order_delivered_customer_date" and "order_status" in df.columns:
                    # Expected missing: statuses other than delivered
                    mask_not_delivered = df["order_status"] != "delivered"
                    mask_delivered = df["order_status"] == "delivered"
                    mask_missing = df[col].isna()
                    
                    expected = int((mask_missing & mask_not_delivered).sum())
                    anomaly = int((mask_missing & mask_delivered).sum())
                    
                    field_analysis["classification"]["EXPECTED_MISSING"] = expected
                    field_analysis["classification"]["POTENTIAL_DATA_QUALITY_ISSUE"] = anomaly

                elif col == "order_delivered_carrier_date" and "order_status" in df.columns:
                    mask_early_status = df["order_status"].isin(["created", "approved", "invoiced", "processing", "canceled", "unavailable"])
                    mask_late_status = df["order_status"].isin(["shipped", "delivered"])
                    mask_missing = df[col].isna()
                    
                    expected = int((mask_missing & mask_early_status).sum())
                    anomaly = int((mask_missing & mask_late_status).sum())
                    
                    field_analysis["classification"]["EXPECTED_MISSING"] = expected
                    field_analysis["classification"]["POTENTIAL_DATA_QUALITY_ISSUE"] = anomaly

                elif col == "order_approved_at":
                    # Any missing approved_at is considered an issue because it acts as a demand anchor
                    field_analysis["classification"]["POTENTIAL_DATA_QUALITY_ISSUE"] = missing_count
                    field_analysis["classification"]["EXPECTED_MISSING"] = 0

            elif dataset_name == "products":
                if col in ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]:
                    # Missing physical dimensions are issues if we need them for volume calcs
                    field_analysis["classification"]["POTENTIAL_DATA_QUALITY_ISSUE"] = missing_count
                    
            results["fields"][col] = field_analysis
            
        return results

    def apply_treatment(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """
        Applies missing value treatment to the dataset based on defined policies.
        Currently, the strict policy is RETAIN_AS_NULL (no statistical imputation, no dropping).
        Returns a new DataFrame.
        """
        df_treated = df.copy()
        
        # In the future, if specific EXCLUDE or IMPUTE logic is added, it goes here.
        # For now, everything is RETAIN_AS_NULL, meaning we do not alter the NaNs.
        # We will enforce this by simply logging that it was retained.
        
        return df_treated
