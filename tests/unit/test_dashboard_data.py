import pytest
import os
import pandas as pd
from src.visualization.dashboard_data import DashboardDataBuilder

@pytest.fixture
def builder():
    return DashboardDataBuilder(
        baseline_dir="data/results/baseline",
        scenarios_dir="data/results/scenarios",
        analysis_dir="data/results/analysis"
    )

def test_dashboard_kpis_build(builder):
    df = builder.build_dashboard_kpis()
    assert len(df) == 6 # baseline + 5 scenarios
    
    expected_cols = [
        "scenario", "scenario_label", "orders_processed", "mean_flow_time_seconds", 
        "mean_flow_time_hours", "median_flow_time_seconds", "p95_flow_time_seconds", 
        "p99_flow_time_seconds", "mean_processing_time_seconds", "mean_waiting_time_seconds", 
        "mean_waiting_time_hours", "sla_achievement_percent", "sla_breach_count"
    ]
    for c in expected_cols:
        assert c in df.columns
        
    assert list(df["scenario"]) == ["baseline", "dispatch_plus_1", "picking_plus_5", "packing_plus_2", "productivity_plus_10", "extended_shift"]

def test_stage_metrics_build(builder):
    df = builder.build_stage_metrics()
    assert len(df) == 30 # 6 scenarios * 5 stages
    
    expected_cols = [
        "scenario", "scenario_label", "stage", "stage_sequence", "worker_count",
        "utilization_percent", "mean_queue", "p95_queue", "max_queue",
        "mean_processing_time_seconds", "mean_waiting_time_seconds"
    ]
    for c in expected_cols:
        assert c in df.columns
        
    assert set(df["stage"]) == {"PROCESSING", "PICKING", "PACKING", "SORTING", "DISPATCH"}
    assert set(df["stage_sequence"]) == {1, 2, 3, 4, 5}

def test_scenario_comparison_build(builder):
    df = builder.build_scenario_comparison()
    assert len(df) == 5 # 5 scenarios, no baseline
    
    expected_cols = [
        "scenario", "scenario_type", "description", "mean_flow_time_seconds",
        "mean_flow_time_change_seconds", "mean_flow_time_change_percent",
        "p95_flow_time_seconds", "p95_flow_time_change_percent",
        "mean_waiting_time_seconds", "mean_waiting_time_change_seconds",
        "mean_waiting_time_change_percent", "sla_achievement_percent", "hypothesis_result"
    ]
    for c in expected_cols:
        assert c in df.columns

def test_intervention_ranking_build(builder):
    df = builder.build_intervention_ranking()
    assert len(df) == 5
    
    expected_cols = [
        "rank", "scenario", "intervention_category", "mean_flow_time_improvement_percent",
        "mean_waiting_time_improvement_percent", "p95_flow_time_improvement_percent",
        "bottleneck_effect", "hypothesis_result", "recommendation_priority"
    ]
    for c in expected_cols:
        assert c in df.columns
        
    # Check that rank is 1..5
    assert list(df["rank"]) == [1, 2, 3, 4, 5]

def test_bottleneck_summary_build(builder):
    df = builder.build_bottleneck_summary()
    assert len(df) == 5
    
    expected_cols = [
        "stage", "utilization_percent", "mean_queue", "p95_queue", 
        "mean_waiting_time_seconds", "bottleneck_score", "bottleneck_rank", "bottleneck_role"
    ]
    for c in expected_cols:
        assert c in df.columns
        
    assert df.iloc[0]["stage"] == "DISPATCH"
    assert df.iloc[0]["bottleneck_rank"] == 1
