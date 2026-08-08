import pandas as pd
from typing import Dict, Any, List

class TimestampValidator:
    """
    Validates temporal integrity of Olist datasets. 
    Identifies missing timestamps, invalid sequences, and date ranges without modifying records.
    """
    
    def __init__(self):
        pass
        
    def validate_orders_timestamps(self, df_orders: pd.DataFrame) -> Dict[str, Any]:
        """
        Runs validation rules on the orders dataset.
        Assumes the dataset has already been standardized by DataStandardizer.
        """
        results = {
            "missingness": {},
            "date_ranges": {},
            "rules": {},
            "status_analysis": {}
        }
        
        # 1. Missingness
        cols = [
            "order_purchase_timestamp", 
            "order_approved_at", 
            "order_delivered_carrier_date", 
            "order_delivered_customer_date", 
            "order_estimated_delivery_date"
        ]
        
        total_records = len(df_orders)
        
        for col in cols:
            if col in df_orders.columns:
                missing = int(df_orders[col].isna().sum())
                results["missingness"][col] = {
                    "missing": missing,
                    "percentage": (missing / total_records) * 100 if total_records > 0 else 0
                }
                
                # Date ranges (min/max excluding NaT)
                valid_dates = df_orders[col].dropna()
                if not valid_dates.empty:
                    results["date_ranges"][col] = {
                        "min": str(valid_dates.min()),
                        "max": str(valid_dates.max())
                    }
                else:
                    results["date_ranges"][col] = {"min": None, "max": None}
                    
        # 2. Validation Rules
        def eval_rule(name: str, desc: str, col_start: str, col_end: str):
            if col_start in df_orders.columns and col_end in df_orders.columns:
                # Only evaluate where both are present
                mask_both_present = df_orders[col_start].notna() & df_orders[col_end].notna()
                evaluated = int(mask_both_present.sum())
                
                if evaluated > 0:
                    passed = int((df_orders.loc[mask_both_present, col_start] <= df_orders.loc[mask_both_present, col_end]).sum())
                    failed = evaluated - passed
                else:
                    passed = 0
                    failed = 0
                    
                missing = total_records - evaluated
                
                results["rules"][name] = {
                    "description": desc,
                    "evaluated": evaluated,
                    "passed": passed,
                    "failed": failed,
                    "missing_or_unavailable": missing,
                    "failure_percentage": (failed / evaluated) * 100 if evaluated > 0 else 0
                }
                
        eval_rule("Rule A", "purchase <= approved", "order_purchase_timestamp", "order_approved_at")
        eval_rule("Rule B", "approved <= delivered_carrier", "order_approved_at", "order_delivered_carrier_date")
        eval_rule("Rule C", "delivered_carrier <= delivered_customer", "order_delivered_carrier_date", "order_delivered_customer_date")
        eval_rule("Rule D", "purchase <= delivered_customer", "order_purchase_timestamp", "order_delivered_customer_date")
        eval_rule("Rule E", "delivered_customer <= estimated_delivery", "order_delivered_customer_date", "order_estimated_delivery_date")
        
        # 3. Status-based missingness analysis (specifically delivered_customer vs status)
        if "order_status" in df_orders.columns and "order_delivered_customer_date" in df_orders.columns:
            status_missing = df_orders.groupby("order_status")["order_delivered_customer_date"].apply(lambda x: x.isna().sum()).to_dict()
            status_total = df_orders.groupby("order_status").size().to_dict()
            
            for status in status_total.keys():
                results["status_analysis"][status] = {
                    "total": int(status_total[status]),
                    "missing_delivery_date": int(status_missing[status])
                }
                
        return results

    def validate_order_items_timestamps(self, df_items: pd.DataFrame, df_orders: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Validates order_items timestamps (shipping_limit_date).
        """
        results = {
            "missingness": {},
            "date_ranges": {},
            "rules": {}
        }
        
        total_records = len(df_items)
        col = "shipping_limit_date"
        
        if col in df_items.columns:
            missing = int(df_items[col].isna().sum())
            results["missingness"][col] = {
                "missing": missing,
                "percentage": (missing / total_records) * 100 if total_records > 0 else 0
            }
            
            valid_dates = df_items[col].dropna()
            if not valid_dates.empty:
                results["date_ranges"][col] = {
                    "min": str(valid_dates.min()),
                    "max": str(valid_dates.max())
                }
            else:
                results["date_ranges"][col] = {"min": None, "max": None}
                
        if df_orders is not None and "order_id" in df_items.columns and "order_id" in df_orders.columns:
            # Merge to check cross-dataset rule: shipping_limit_date vs order_approved_at
            # shipping_limit_date is usually after order_approved_at
            merged = df_items[["order_id", "shipping_limit_date"]].merge(
                df_orders[["order_id", "order_approved_at"]], on="order_id", how="inner"
            )
            
            mask_both = merged["order_approved_at"].notna() & merged["shipping_limit_date"].notna()
            evaluated = int(mask_both.sum())
            
            if evaluated > 0:
                passed = int((merged.loc[mask_both, "order_approved_at"] <= merged.loc[mask_both, "shipping_limit_date"]).sum())
                failed = evaluated - passed
            else:
                passed = 0
                failed = 0
                
            missing_count = len(df_items) - evaluated
            
            results["rules"]["Item Rule A"] = {
                "description": "order_approved_at <= shipping_limit_date",
                "evaluated": evaluated,
                "passed": passed,
                "failed": failed,
                "missing_or_unavailable": missing_count,
                "failure_percentage": (failed / evaluated) * 100 if evaluated > 0 else 0
            }

        return results
