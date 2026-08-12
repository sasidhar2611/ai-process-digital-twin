import pytest
import os
import pandas as pd

def test_executive_summary_data_loading():
    # Verify the dashboard loads from the correct analytical datasets
    assert os.path.exists("data/dashboard/dashboard_kpis.csv")
    assert os.path.exists("data/dashboard/dashboard_bottleneck_summary.csv")
    assert os.path.exists("data/dashboard/dashboard_intervention_ranking.csv")
    assert os.path.exists("data/dashboard/dashboard_stage_metrics.csv")

def test_executive_summary_kpi_extraction():
    kpi_df = pd.read_csv("data/dashboard/dashboard_kpis.csv")
    baseline_kpi = kpi_df[kpi_df["scenario"] == "baseline"]
    assert not baseline_kpi.empty
    
    row = baseline_kpi.iloc[0]
    assert "mean_flow_time_seconds" in row
    assert "mean_processing_time_seconds" in row
    assert row["mean_flow_time_seconds"] > 0
    
    # Efficiency is processing / flow
    efficiency = (row["mean_processing_time_seconds"] / row["mean_flow_time_seconds"]) * 100
    assert efficiency > 0 and efficiency < 100

def test_executive_summary_bottleneck_extraction():
    bn_df = pd.read_csv("data/dashboard/dashboard_bottleneck_summary.csv")
    primary_bn = bn_df[bn_df["bottleneck_role"] == "Active Process Bottleneck"]
    assert not primary_bn.empty
    assert primary_bn.iloc[0]["stage"] == "DISPATCH"

def test_executive_summary_intervention_extraction():
    inv_df = pd.read_csv("data/dashboard/dashboard_intervention_ranking.csv")
    assert not inv_df.empty
    best_scenario = inv_df.sort_values("mean_flow_time_improvement_percent", ascending=False).iloc[0]
    # Extended shift or dispatch+1 is expected to be best depending on runs, extended_shift is usually ~27%
    assert best_scenario["mean_flow_time_improvement_percent"] > 0
