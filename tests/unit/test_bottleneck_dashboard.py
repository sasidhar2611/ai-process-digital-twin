import pytest
import os
import pandas as pd

def test_bottleneck_dashboard_files_exist():
    assert os.path.exists("data/dashboard/dashboard_bottleneck_summary.csv")
    assert os.path.exists("data/dashboard/dashboard_intervention_ranking.csv")
    assert os.path.exists("data/dashboard/dashboard_stage_metrics.csv")

def test_bottleneck_identification():
    # Verify DISPATCH is correctly identified as the baseline bottleneck
    df = pd.read_csv("data/dashboard/dashboard_bottleneck_summary.csv")
    active_bottleneck = df[df["bottleneck_role"] == "Active Process Bottleneck"].iloc[0]
    assert active_bottleneck["stage"] == "DISPATCH"
    assert active_bottleneck["bottleneck_rank"] == 1

def test_intervention_ranking_exists():
    df = pd.read_csv("data/dashboard/dashboard_intervention_ranking.csv")
    assert not df.empty
    expected_cols = [
        "rank", "scenario", "intervention_category", 
        "mean_flow_time_improvement_percent", "bottleneck_effect"
    ]
    for c in expected_cols:
        assert c in df.columns
