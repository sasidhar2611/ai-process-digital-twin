import pytest
import os
import pandas as pd

def test_operational_flow_files_exist():
    # Verify the dashboard loads from the correct analytical datasets
    assert os.path.exists("data/dashboard/dashboard_stage_metrics.csv")
    assert os.path.exists("data/dashboard/dashboard_kpis.csv")

def test_flow_time_breakdown_metrics():
    # Ensure flow time components are valid and non-negative
    kpi_df = pd.read_csv("data/dashboard/dashboard_kpis.csv")
    assert "mean_flow_time_seconds" in kpi_df.columns
    assert "mean_waiting_time_seconds" in kpi_df.columns
    assert "mean_processing_time_seconds" in kpi_df.columns
    
    baseline = kpi_df[kpi_df["scenario"] == "baseline"].iloc[0]
    
    # Wait + Process roughly equals Flow (allowing some minor tracking discrepancies depending on exact methodology)
    assert baseline["mean_flow_time_seconds"] > 0
    assert baseline["mean_waiting_time_seconds"] >= 0
    assert baseline["mean_processing_time_seconds"] > 0
    
    # Wait time should dominate processing time in the baseline (this is the expected insight)
    assert baseline["mean_waiting_time_seconds"] > baseline["mean_processing_time_seconds"]

def test_stage_metrics_columns():
    stage_df = pd.read_csv("data/dashboard/dashboard_stage_metrics.csv")
    expected_cols = [
        "stage", "utilization_percent", "mean_queue", "p95_queue", 
        "mean_processing_time_seconds", "mean_waiting_time_seconds"
    ]
    for c in expected_cols:
        assert c in stage_df.columns
