import pytest
import json
import os
import pandas as pd
from src.synthetic.scenario import ScenarioManager, ScenarioDefinition
from src.synthetic.config import SyntheticModelConfiguration

def test_shift_factor_change():
    with open("config/scenarios/baseline.json", "r") as f:
        baseline_data = json.load(f)
        baseline = ScenarioDefinition.load_from_dict(baseline_data)
        
    with open("config/scenarios/extended_shift.json", "r") as f:
        scenario_data = json.load(f)
        scenario = ScenarioDefinition.load_from_dict(scenario_data)
        
    assert baseline.configuration.worker_config.shift_hours == (8, 18)
    assert scenario.configuration.worker_config.shift_hours == (7, 19)

def test_no_other_baseline_parameter_changes():
    with open("config/scenarios/baseline.json", "r") as f:
        baseline_data = json.load(f)
        
    with open("config/scenarios/extended_shift.json", "r") as f:
        scenario_data = json.load(f)
        
    b_conf = baseline_data["configuration"]
    s_conf = scenario_data["configuration"]
    
    assert b_conf["version"] == s_conf["version"]
    assert b_conf["random_seed"] == s_conf["random_seed"]
    assert b_conf["queue_policy"] == s_conf["queue_policy"]
    assert b_conf["productivity_factor"] == s_conf["productivity_factor"]
    
    b_workers = b_conf["worker_config"]
    s_workers = s_conf["worker_config"]
    assert b_workers["dynamic_reallocation"] == s_workers["dynamic_reallocation"]
    
    for stage in b_workers["stages_assigned"]:
        assert b_workers["stages_assigned"][stage] == s_workers["stages_assigned"][stage]
            
    assert b_conf["stages"] == s_conf["stages"]

def test_baseline_configuration_immutable():
    baseline_config = SyntheticModelConfiguration()
    manager = ScenarioManager(baseline_config)
    
    initial_shift = baseline_config.worker_config.shift_hours
    
    scenario = manager.create_scenario(
        "test", "test", "SHIFT_SCENARIO", "test", {"shift_hours": [7, 19]}
    )
    
    assert baseline_config.worker_config.shift_hours == initial_shift
    assert scenario.configuration.worker_config.shift_hours == (7, 19)

def test_comparison_metrics_calculation():
    if not os.path.exists("data/results/scenarios/baseline_vs_extended_shift.json"):
        pytest.skip("Comparison file not generated yet")
        
    with open("data/results/scenarios/baseline_vs_extended_shift.json", "r") as f:
        comparison = json.load(f)
        
    metric = comparison.get("orders_processed")
    if metric:
        assert metric["absolute_change"] == metric["extended_shift"] - metric["baseline"]
        if metric["baseline"] == 0:
            assert metric["percentage_change"] == 0
        else:
            assert abs(metric["percentage_change"] - (metric["absolute_change"] / metric["baseline"] * 100)) < 0.001
