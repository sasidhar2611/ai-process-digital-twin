import pandas as pd
import numpy as np
from typing import Dict, Any, List

class KPIExtractor:
    """
    Extracts Key Performance Indicators from a synthetic operational dataset.
    """
    def __init__(self, df_syn: pd.DataFrame, df_orders: pd.DataFrame, shift_hours: tuple = (8, 18), sla_seconds: float = 432000.0):
        self.df_syn = df_syn.copy()
        self.df_orders = df_orders.copy()
        self.shift_hours = shift_hours
        self.shift_duration_seconds = (shift_hours[1] - shift_hours[0]) * 3600
        
        # SLA assumption: 5 days = 432,000 seconds
        self.sla_seconds = sla_seconds
        
    def calculate_order_metrics(self) -> pd.DataFrame:
        """
        Calculate metrics at the order level.
        """
        # Aggregate processing and waiting times per order
        agg = self.df_syn.groupby("order_id").agg({
            "processing_time": "sum",
            "waiting_time": "sum",
        }).rename(columns={
            "processing_time": "total_processing_time",
            "waiting_time": "total_waiting_time"
        })
        
        # Get final dispatch end time
        dispatch = self.df_syn[self.df_syn["stage_sequence"] == 5][["order_id", "end_time"]].rename(columns={"end_time": "dispatch_end_time"})
        
        # Merge to get demand release time
        orders_subset = self.df_orders[["order_id", "order_approved_at"]].rename(columns={"order_approved_at": "demand_release_time"})
        
        metrics = agg.merge(dispatch, on="order_id", how="inner")
        metrics = metrics.merge(orders_subset, on="order_id", how="inner")
        
        # Calculate flow time
        metrics["flow_time"] = (metrics["dispatch_end_time"] - metrics["demand_release_time"]).dt.total_seconds()
        
        # Calculate SLA
        metrics["sla_met"] = metrics["flow_time"] <= self.sla_seconds
        
        # Safety checks
        metrics["flow_time"] = metrics["flow_time"].clip(lower=0)
        
        return metrics
        
    def calculate_stage_metrics(self) -> pd.DataFrame:
        """
        Calculate metrics at the stage level including utilization.
        """
        # 1. Base aggregations
        agg = self.df_syn.groupby("stage").agg({
            "order_id": "count",
            "processing_time": ["mean", lambda x: np.percentile(x, 95), "sum"],
            "waiting_time": ["mean", lambda x: np.percentile(x, 95)],
            "queue_length": ["mean", lambda x: np.percentile(x, 95), "max"],
            "worker_count": "first",
            "start_time": ["min"],
            "end_time": ["max"]
        })
        
        agg.columns = [
            "orders_processed",
            "mean_processing_time", "p95_processing_time", "total_processing_time_sum",
            "mean_waiting_time", "p95_waiting_time",
            "mean_queue_length", "p95_queue_length", "max_queue_length",
            "worker_count",
            "min_start", "max_end"
        ]
        agg = agg.reset_index()
        
        # Reorder based on sequence
        stage_order = {"PROCESSING": 1, "PICKING": 2, "PACKING": 3, "SORTING": 4, "DISPATCH": 5}
        agg["stage_sequence"] = agg["stage"].map(stage_order)
        agg = agg.sort_values("stage_sequence")
        
        # Calculate Utilization
        # To find active simulation days per stage, we find unique dates where work started
        def calc_util(row, df_syn):
            st = row["stage"]
            st_df = df_syn[df_syn["stage"] == st]
            # Active days based on start_time
            active_days = st_df["start_time"].dt.date.nunique()
            if active_days == 0 or row["worker_count"] == 0:
                return 0.0
                
            available_time_seconds = row["worker_count"] * self.shift_duration_seconds * active_days
            busy_time = row["total_processing_time_sum"]
            
            return busy_time / available_time_seconds
            
        agg["stage_utilization"] = agg.apply(lambda r: calc_util(r, self.df_syn), axis=1)
        agg["worker_utilization"] = agg["stage_utilization"] # Same structurally in this model without dynamic reassignment
        
        # Format output
        cols_to_keep = [
            "stage", "stage_sequence", "worker_count", "orders_processed",
            "mean_processing_time", "p95_processing_time",
            "mean_waiting_time", "p95_waiting_time",
            "mean_queue_length", "p95_queue_length", "max_queue_length",
            "worker_utilization", "stage_utilization"
        ]
        
        return agg[cols_to_keep]
        
    def generate_summary(self, scenario_id: str, order_metrics: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate overall KPI summary dict.
        """
        if len(order_metrics) == 0:
            return {}
            
        ft = order_metrics["flow_time"]
        
        return {
            "scenario_id": scenario_id,
            "orders_processed": int(len(order_metrics)),
            "mean_flow_time": float(ft.mean()),
            "median_flow_time": float(ft.median()),
            "p95_flow_time": float(ft.quantile(0.95)),
            "p99_flow_time": float(ft.quantile(0.99)),
            "mean_processing_time": float(order_metrics["total_processing_time"].mean()),
            "mean_waiting_time": float(order_metrics["total_waiting_time"].mean()),
            "sla_achievement_percentage": float(order_metrics["sla_met"].mean() * 100),
            "sla_breach_count": int((~order_metrics["sla_met"]).sum()),
            "total_simulation_time": float((self.df_syn["end_time"].max() - self.df_syn["start_time"].min()).total_seconds())
        }
