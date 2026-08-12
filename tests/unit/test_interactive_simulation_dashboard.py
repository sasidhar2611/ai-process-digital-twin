import pytest
import os
import pandas as pd

def test_simulation_data_exists():
    assert os.path.exists("data/dashboard/dashboard_scenario_comparison.csv")
    assert os.path.exists("data/dashboard/dashboard_kpis.csv")
    assert os.path.exists("data/dashboard/dashboard_stage_metrics.csv")

def test_available_scenarios():
    comp_df = pd.read_csv("data/dashboard/dashboard_scenario_comparison.csv")
    labels = comp_df["scenario_label"].tolist()
    assert "Dispatch +1 Worker" in labels
    assert "Picking +5 Workers" in labels
    assert "Packing +2 Workers" in labels
    assert "Productivity +10%" in labels
    assert "Extended Shift" in labels

def test_percentage_change_consistency():
    comp_df = pd.read_csv("data/dashboard/dashboard_scenario_comparison.csv")
    kpi_df = pd.read_csv("data/dashboard/dashboard_kpis.csv")
    
    baseline_val = kpi_df[kpi_df["scenario"] == "baseline"]["mean_flow_time_seconds"].values[0]
    ext_shift_row = comp_df[comp_df["scenario"] == "extended_shift"].iloc[0]
    ext_val = ext_shift_row["mean_flow_time_seconds"]
    
    expected_change = ((ext_val - baseline_val) / baseline_val) * 100
    assert abs(ext_shift_row["mean_flow_time_change_percent"] - expected_change) < 0.1

def test_stage_metrics_match():
    # Ensure stage metrics align correctly
    stage_df = pd.read_csv("data/dashboard/dashboard_stage_metrics.csv")
    dispatch_base = stage_df[(stage_df["scenario"] == "baseline") & (stage_df["stage"] == "DISPATCH")]
    assert not dispatch_base.empty
    
    dispatch_scen = stage_df[(stage_df["scenario"] == "dispatch_plus_1") & (stage_df["stage"] == "DISPATCH")]
    assert not dispatch_scen.empty
    
    # We expect dispatch queue to be significantly lower in the scenario
    assert dispatch_scen["mean_queue"].values[0] < dispatch_base["mean_queue"].values[0]
