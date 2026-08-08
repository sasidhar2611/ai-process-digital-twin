import pandas as pd
import numpy as np
from typing import Dict, Any, List

class SyntheticValidator:
    """
    Validates synthetic operational data structurally, temporally, and statistically.
    """
    def __init__(self, df_syn: pd.DataFrame, df_orders: pd.DataFrame):
        self.df_syn = df_syn
        self.df_orders = df_orders
        
    def validate_structure(self) -> Dict[str, Any]:
        results = {}
        # 1. order_id linkage
        syn_orders = set(self.df_syn["order_id"].unique())
        processed_orders = set(self.df_orders["order_id"].unique())
        results["all_orders_linked"] = syn_orders.issubset(processed_orders)
        
        # 2. 5 stage records per order
        stage_counts = self.df_syn.groupby("order_id").size()
        results["exactly_five_stages"] = bool((stage_counts == 5).all())
        
        # 3, 4, 5, 6. Stage Sequence Check
        # Check if the set of stage_sequence per order is always {1, 2, 3, 4, 5}
        # and stage names match the sequence exactly.
        expected_stages = {1: "PROCESSING", 2: "PICKING", 3: "PACKING", 4: "SORTING", 5: "DISPATCH"}
        
        seq_valid = True
        name_valid = True
        
        # We can do this efficiently
        # Group by sequence and check unique names
        for seq, name in expected_stages.items():
            subset = self.df_syn[self.df_syn["stage_sequence"] == seq]
            if not (subset["stage"] == name).all():
                name_valid = False
                
        # Check if every order has exactly sequence 1,2,3,4,5
        seq_sums = self.df_syn.groupby("order_id")["stage_sequence"].sum()
        if not (seq_sums == 15).all(): # 1+2+3+4+5 = 15
            seq_valid = False
            
        results["sequence_valid"] = seq_valid
        results["names_valid"] = name_valid
        
        return results

    def validate_temporal(self) -> Dict[str, Any]:
        results = {}
        # processing >= 0
        results["processing_time_valid"] = bool((self.df_syn["processing_time"] >= 0).all())
        # waiting >= 0
        results["waiting_time_valid"] = bool((self.df_syn["waiting_time"] >= 0).all())
        # end >= start
        results["end_ge_start"] = bool((self.df_syn["end_time"] >= self.df_syn["start_time"]).all())
        
        # end = start + processing
        calc_end = self.df_syn["start_time"] + pd.to_timedelta(self.df_syn["processing_time"], unit='s')
        # floating point tolerance
        diff = (self.df_syn["end_time"] - calc_end).dt.total_seconds().abs()
        results["end_equals_start_plus_proc"] = bool((diff < 1.0).all())
        
        # Continuity: stage N+1 start >= stage N end
        # We can sort and shift
        df_sorted = self.df_syn.sort_values(["order_id", "stage_sequence"])
        df_sorted["prev_end"] = df_sorted.groupby("order_id")["end_time"].shift(1)
        
        # for sequence > 1, start_time >= prev_end
        mask = df_sorted["stage_sequence"] > 1
        continuity_diff = (df_sorted.loc[mask, "start_time"] - df_sorted.loc[mask, "prev_end"]).dt.total_seconds()
        results["stage_continuity_valid"] = bool((continuity_diff >= -1.0).all()) # allow small fp diff
        
        # Stage 1 start >= order_approved_at
        s1 = df_sorted[df_sorted["stage_sequence"] == 1].copy()
        s1 = s1.merge(self.df_orders[["order_id", "order_approved_at"]], on="order_id", how="left")
        results["start_after_approval"] = bool((s1["start_time"] >= s1["order_approved_at"]).all())
        
        return results

    def validate_shift(self, shift_start=8, shift_end=18) -> Dict[str, Any]:
        # active processing occurs only 08:00 - 18:00
        # A task might cross shift boundary in the simple generator, or it might just start during shift
        # Actually our generator only forces `start_time` to be within shift.
        # It allows `end_time` to cross 18:00 for simplicity (it doesn't pause the task).
        # Let's check `start_time` compliance.
        hours = self.df_syn["start_time"].dt.hour
        results = {
            "start_time_in_shift": bool(((hours >= shift_start) & (hours < shift_end)).all())
        }
        return results
        
    def validate_resources(self) -> Dict[str, Any]:
        results = {}
        results["worker_count_valid"] = bool((self.df_syn["worker_count"] >= 1).all())
        results["queue_length_valid"] = bool((self.df_syn["queue_length"] >= 0).all())
        results["productivity_valid"] = bool((self.df_syn["productivity_factor"] > 0).all())
        return results

    def calculate_statistics(self) -> Dict[str, Any]:
        stats = {"stages": {}}
        
        for seq in sorted(self.df_syn["stage_sequence"].unique()):
            st = self.df_syn[self.df_syn["stage_sequence"] == seq]
            name = st["stage"].iloc[0]
            
            stage_stats = {
                "processing_time": self._describe(st["processing_time"]),
                "waiting_time": self._describe(st["waiting_time"]),
                "queue_length": self._describe(st["queue_length"]),
                "wait_zero_pct": float((st["waiting_time"] == 0).mean() * 100),
                "queue_wait_corr": float(st["queue_length"].corr(st["waiting_time"])) if st["queue_length"].std() > 0 else 0.0
            }
            
            if name == "PICKING":
                stage_stats["corr_item_count"] = float(st["item_count"].corr(st["processing_time"]))
                stage_stats["corr_volume"] = float(st["total_volume_cm3"].corr(st["processing_time"]))
            elif name == "PACKING":
                stage_stats["corr_item_count"] = float(st["item_count"].corr(st["processing_time"]))
                stage_stats["corr_weight"] = float(st["total_weight_g"].corr(st["processing_time"]))
                
            stats["stages"][name] = stage_stats
            
        return stats
        
    def analyze_calibration(self) -> Dict[str, Any]:
        final_stages = self.df_syn[self.df_syn["stage_sequence"] == 5]
        eval_df = final_stages.merge(self.df_orders[["order_id", "order_delivered_carrier_date"]], on="order_id", how="left")
        
        valid_eval = eval_df[eval_df["order_delivered_carrier_date"].notna()].copy()
        valid_eval["completed_before_carrier"] = valid_eval["end_time"] <= valid_eval["order_delivered_carrier_date"]
        
        pct_before = valid_eval["completed_before_carrier"].mean() * 100
        pct_after = 100.0 - pct_before
        
        # Investigate the "after" cases (beyond boundary)
        after_df = valid_eval[~valid_eval["completed_before_carrier"]]
        
        investigation = {
            "mean_item_count": float(after_df["item_count"].mean()),
            "mean_total_weight_g": float(after_df["total_weight_g"].mean()),
            "mean_total_volume_cm3": float(after_df["total_volume_cm3"].mean()),
            "mean_queue_length_dispatch": float(after_df["queue_length"].mean()),
            "mean_waiting_time_dispatch": float(after_df["waiting_time"].mean())
        }
        
        return {
            "total_evaluated": len(valid_eval),
            "completed_before_carrier_pct": float(pct_before),
            "completed_after_carrier_pct": float(pct_after),
            "anomaly_investigation": investigation
        }

    def _describe(self, series: pd.Series) -> Dict[str, float]:
        if len(series) == 0:
            return {}
        return {
            "count": int(series.count()),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "p01": float(series.quantile(0.01)),
            "p05": float(series.quantile(0.05)),
            "p25": float(series.quantile(0.25)),
            "p50": float(series.quantile(0.50)),
            "p75": float(series.quantile(0.75)),
            "p95": float(series.quantile(0.95)),
            "p99": float(series.quantile(0.99))
        }
