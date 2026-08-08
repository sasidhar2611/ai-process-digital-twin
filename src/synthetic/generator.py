import pandas as pd
import numpy as np
import os
import json
import bisect
import time
from typing import Dict, Any, List

from src.synthetic.config import SyntheticModelConfiguration

class SyntheticDataGenerator:
    """
    Generates synthetic operational warehouse data based on real Olist processed datasets.
    """
    def __init__(self, config: SyntheticModelConfiguration):
        self.config = config
        # Set random seed
        np.random.seed(self.config.random_seed)
        
    def _next_working_time(self, t: pd.Timestamp) -> pd.Timestamp:
        """
        Advances timestamp to next working hour if outside the shift.
        Assuming daily shift (including weekends) for simplicity, 
        using config shift_hours (e.g. 8 to 18).
        """
        if pd.isna(t):
            return t
            
        start_h, end_h = self.config.worker_config.shift_hours
        
        # If hour is after or equal to end of shift, move to next day start
        if t.hour >= end_h:
            return (t + pd.Timedelta(days=1)).replace(hour=start_h, minute=0, second=0, microsecond=0)
        # If hour is before start of shift, move to today's start
        elif t.hour < start_h:
            return t.replace(hour=start_h, minute=0, second=0, microsecond=0)
            
        return t

    def generate(self, df_orders: pd.DataFrame, df_products: pd.DataFrame = None, df_items: pd.DataFrame = None) -> pd.DataFrame:
        """
        Generates 5 stages of synthetic data per eligible order.
        """
        # Filter eligible orders
        if "eligible_for_demand_timeline" in df_orders.columns:
            eligible_orders = df_orders[df_orders["eligible_for_demand_timeline"] == True].copy()
        else:
            eligible_orders = df_orders[df_orders["order_approved_at"].notna()].copy()
            
        # Merge product/item data if provided to get drivers
        # In processed data, we might need to aggregate items
        item_agg = None
        if df_items is not None:
            # item count
            item_agg = df_items.groupby("order_id").size().reset_index(name="item_count")
            
            # If products are provided, join to get volume/weight
            if df_products is not None:
                items_prod = df_items.merge(df_products, on="product_id", how="left")
                weight_vol = items_prod.groupby("order_id").agg({
                    "product_weight_g": "sum",
                    "physical_volume_cm3": "sum"
                }).reset_index().rename(columns={
                    "product_weight_g": "total_weight_g",
                    "physical_volume_cm3": "total_volume_cm3"
                })
                item_agg = item_agg.merge(weight_vol, on="order_id", how="left")
                
        if item_agg is not None:
            eligible_orders = eligible_orders.merge(item_agg, on="order_id", how="left")
        else:
            # Provide defaults if missing
            if "item_count" not in eligible_orders.columns:
                eligible_orders["item_count"] = 1
            if "total_weight_g" not in eligible_orders.columns:
                eligible_orders["total_weight_g"] = 1000.0
            if "total_volume_cm3" not in eligible_orders.columns:
                eligible_orders["total_volume_cm3"] = 1000.0
                
        # Fill NaNs in derived features
        eligible_orders["item_count"] = eligible_orders["item_count"].fillna(1).astype(int)
        eligible_orders["total_weight_g"] = eligible_orders["total_weight_g"].fillna(1000.0)
        eligible_orders["total_volume_cm3"] = eligible_orders["total_volume_cm3"].fillna(1000.0)
        
        # We process stages sequentially.
        # Initialize arrival times at stage 1
        current_arrivals = eligible_orders[["order_id", "order_approved_at", "item_count", "total_weight_g", "total_volume_cm3"]].copy()
        # Customer state is not in orders by default, let's assume it's merged or we use a dummy
        if "customer_state" in eligible_orders.columns:
            current_arrivals["customer_state"] = eligible_orders["customer_state"]
        else:
            current_arrivals["customer_state"] = "SP"
            
        current_arrivals = current_arrivals.rename(columns={"order_approved_at": "arrival_time"})
        
        all_stage_records = []
        
        stages = [
            (1, "PROCESSING"),
            (2, "PICKING"),
            (3, "PACKING"),
            (4, "SORTING"),
            (5, "DISPATCH")
        ]
        
        for stage_seq, stage_name in stages:
            stage_config = self.config.stages[stage_seq]
            worker_count = self.config.worker_config.stages_assigned.get(stage_name, 1)
            
            # Sort arrivals chronologically
            current_arrivals = current_arrivals.sort_values("arrival_time")
            
            # Worker availability tracker (list of timestamps, initially early)
            # Use a dummy early date
            early_date = pd.Timestamp("2000-01-01")
            worker_avail = [early_date] * worker_count
            
            stage_records = []
            
            # For queue tracking
            start_times_sorted = []
            
            for i, row in current_arrivals.iterrows():
                arr = row["arrival_time"]
                
                # Assign to earliest available worker
                min_avail_idx = np.argmin(worker_avail)
                worker_avail_time = worker_avail[min_avail_idx]
                
                # Start time is max of arrival and worker availability
                start = max(arr, worker_avail_time)
                
                # Apply shift constraint
                start = self._next_working_time(start)
                
                # Calculate queue length at arrival
                # Number of orders arrived before or at `arr` is just the index in the sorted df (which we can track with a counter)
                # Number of orders started before `arr` can be found using bisect
                started_before_arr = bisect.bisect_right(start_times_sorted, arr)
                queue_length = max(0, len(start_times_sorted) - started_before_arr) # Actually, the counter of processed items so far is len(start_times_sorted). 
                
                # Wait time
                wait = (start - arr).total_seconds()
                
                # Productivity
                # Mean 1.0, slightly varied
                prod_factor = np.clip(np.random.normal(1.0, 0.1), 0.5, 1.5)
                
                # Base processing time & Drivers
                base_time = stage_config.base_processing_seconds
                complexity = 1.0
                
                if "item_count" in stage_config.drivers:
                    complexity *= (1.0 + 0.1 * (row["item_count"] - 1))
                if "total_weight_g" in stage_config.drivers:
                    complexity *= (1.0 + 0.05 * (row["total_weight_g"] / 1000.0))
                if "total_volume_cm3" in stage_config.drivers:
                    complexity *= (1.0 + 0.05 * (row["total_volume_cm3"] / 10000.0))
                    
                # Lognormal noise (sigma = 0.2)
                noise = np.random.lognormal(mean=0.0, sigma=0.2)
                
                proc_time = (base_time * complexity * noise) / prod_factor
                
                end = start + pd.Timedelta(seconds=proc_time)
                
                # Update worker
                worker_avail[min_avail_idx] = end
                
                # Maintain sorted start times for queue calculation
                bisect.insort(start_times_sorted, start)
                
                record = {
                    "order_id": row["order_id"],
                    "stage": stage_name,
                    "stage_sequence": stage_seq,
                    "start_time": start,
                    "end_time": end,
                    "processing_time": proc_time,
                    "waiting_time": wait,
                    "worker_id": min_avail_idx + 1,
                    "worker_count": worker_count,
                    "productivity_factor": prod_factor,
                    "queue_length": queue_length,
                    
                    # retain context
                    "item_count": row["item_count"],
                    "total_weight_g": row["total_weight_g"],
                    "total_volume_cm3": row["total_volume_cm3"]
                }
                stage_records.append(record)
                
            # Create df for this stage to prepare arrivals for next stage
            df_stage = pd.DataFrame(stage_records)
            all_stage_records.append(df_stage)
            
            # Next stage arrivals are the end times of this stage
            current_arrivals["arrival_time"] = df_stage["end_time"].values
            
        df_final = pd.concat(all_stage_records, ignore_index=True)
        # Sort by order_id and stage_sequence
        df_final = df_final.sort_values(["order_id", "stage_sequence"]).reset_index(drop=True)
        return df_final
