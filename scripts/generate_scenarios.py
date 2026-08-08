import os
import json
from src.synthetic.config import SyntheticModelConfiguration
from src.synthetic.scenario import ScenarioManager

def main():
    os.makedirs("config/scenarios", exist_ok=True)
    
    baseline_config = SyntheticModelConfiguration()
    manager = ScenarioManager(baseline_config)
    
    scenarios = []
    
    # 1. BASELINE
    scenarios.append(manager.create_scenario(
        scenario_id="baseline",
        scenario_name="Baseline Configuration",
        scenario_type="BASELINE",
        description="Exact replica of the Module 5.2 validation baseline.",
        parameter_changes={}
    ))
    
    # 2. DISPATCH_PLUS_1
    scenarios.append(manager.create_scenario(
        scenario_id="dispatch_plus_1",
        scenario_name="Dispatch Capacity +1",
        scenario_type="CAPACITY_SCENARIO",
        description="Increases dispatch workers from 3 to 4 to reduce shift-rollover queues.",
        parameter_changes={"worker_counts": {"DISPATCH": 4}}
    ))
    
    # 3. PICKING_PLUS_5
    scenarios.append(manager.create_scenario(
        scenario_id="picking_plus_5",
        scenario_name="Picking Capacity +5",
        scenario_type="CAPACITY_SCENARIO",
        description="Increases picking workers from 15 to 20.",
        parameter_changes={"worker_counts": {"PICKING": 20}}
    ))
    
    # 4. PACKING_PLUS_2
    scenarios.append(manager.create_scenario(
        scenario_id="packing_plus_2",
        scenario_name="Packing Capacity +2",
        scenario_type="CAPACITY_SCENARIO",
        description="Increases packing workers from 10 to 12.",
        parameter_changes={"worker_counts": {"PACKING": 12}}
    ))
    
    # 5. PRODUCTIVITY_PLUS_10
    scenarios.append(manager.create_scenario(
        scenario_id="productivity_plus_10",
        scenario_name="Productivity +10%",
        scenario_type="PRODUCTIVITY_SCENARIO",
        description="Applies a 10% global speed increase (1.10 multiplier).",
        parameter_changes={"productivity_factor": 1.10}
    ))
    
    # 6. EXTENDED_SHIFT
    scenarios.append(manager.create_scenario(
        scenario_id="extended_shift",
        scenario_name="Extended Shift (12h)",
        scenario_type="SHIFT_SCENARIO",
        description="Extends operating shift from 08:00-18:00 to 07:00-19:00.",
        parameter_changes={"shift_hours": (7, 19)}
    ))
    
    for s in scenarios:
        path = f"config/scenarios/{s.scenario_id}.json"
        with open(path, "w") as f:
            f.write(s.serialize())
        print(f"Generated {path}")

if __name__ == "__main__":
    main()
