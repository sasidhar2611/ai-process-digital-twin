import pytest
import json
import os
import pandas as pd
from src.synthetic.scenario import ScenarioManager, ScenarioDefinition
from src.synthetic.config import SyntheticModelConfiguration

def test_picking_worker_count_change():
    with open("config/scenarios/baseline.json", "r") as f:
        baseline_data = json.load(f)
        baseline = ScenarioDefinition.load_from_dict(baseline_data)
        
    with open("config/scenarios/picking_plus_5.json", "r") as f:
        scenario_data = json.load(f)
        scenario = ScenarioDefinition.load_from_dict(scenario_data)
        
    assert baseline.configuration.worker_config.stages_assigned["PICKING"] == 15
    assert scenario.configuration.worker_config.stages_assigned["PICKING"] == 20

def test_no_other_baseline_parameter_changes():
    with open("config/scenarios/baseline.json", "r") as f:
        baseline_data = json.load(f)
        
    with open("config/scenarios/picking_plus_5.json", "r") as f:
        scenario_data = json.load(f)
        
    b_conf = baseline_data["configuration"]
    s_conf = scenario_data["configuration"]
    
    assert b_conf["version"] == s_conf["version"]
    assert b_conf["random_seed"] == s_conf["random_seed"]
    assert b_conf["queue_policy"] == s_conf["queue_policy"]
    assert b_conf["productivity_factor"] == s_conf["productivity_factor"]
    
    b_workers = b_conf["worker_config"]
    s_workers = s_conf["worker_config"]
    assert b_workers["shift_hours"] == s_workers["shift_hours"]
    assert b_workers["dynamic_reallocation"] == s_workers["dynamic_reallocation"]
    
    for stage in b_workers["stages_assigned"]:
        if stage != "PICKING":
            assert b_workers["stages_assigned"][stage] == s_workers["stages_assigned"][stage]
            
    assert b_conf["stages"] == s_conf["stages"]

def test_baseline_configuration_immutable():
    baseline_config = SyntheticModelConfiguration()
    manager = ScenarioManager(baseline_config)
    
    initial_picking = baseline_config.worker_config.stages_assigned["PICKING"]
    
    scenario = manager.create_scenario(
        "test", "test", "CAPACITY_SCENARIO", "test", {"worker_counts": {"PICKING": 20}}
    )
    
    assert baseline_config.worker_config.stages_assigned["PICKING"] == initial_picking
    assert scenario.configuration.worker_config.stages_assigned["PICKING"] == 20

def test_comparison_metrics_calculation():
    if not os.path.exists("data/results/scenarios/baseline_vs_picking_plus_5.json"):
        pytest.skip("Comparison file not generated yet")
        
    with open("data/results/scenarios/baseline_vs_picking_plus_5.json", "r") as f:
        comparison = json.load(f)
        
    metric = comparison.get("orders_processed")
    if metric:
        assert metric["absolute_change"] == metric["picking_plus_5"] - metric["baseline"]
        if metric["baseline"] == 0:
            assert metric["percentage_change"] == 0
        else:
            assert abs(metric["percentage_change"] - (metric["absolute_change"] / metric["baseline"] * 100)) < 0.001
