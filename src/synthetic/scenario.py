import json
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from copy import deepcopy
import datetime
from src.synthetic.config import SyntheticModelConfiguration, StageConfiguration, WorkerConfiguration

SCENARIO_TYPES = [
    "BASELINE",
    "CAPACITY_SCENARIO",
    "PRODUCTIVITY_SCENARIO",
    "SHIFT_SCENARIO",
    "DEMAND_SCENARIO",
    "VARIABILITY_SCENARIO",
    "COMBINED_SCENARIO"
]

@dataclass
class ScenarioDefinition:
    scenario_id: str
    scenario_name: str
    scenario_type: str
    description: str
    base_config_version: str
    model_version: str
    random_seed: int
    parameter_changes: Dict[str, Any]
    created_at: str
    configuration: SyntheticModelConfiguration
    
    def validate(self):
        """Validate the constraints on the scenario."""
        if self.scenario_type not in SCENARIO_TYPES:
            raise ValueError(f"Invalid scenario type: {self.scenario_type}")
            
        if self.configuration.worker_config.shift_hours[0] >= self.configuration.worker_config.shift_hours[1]:
            raise ValueError("Shift start must be before shift end.")
            
        if self.configuration.productivity_factor <= 0:
            raise ValueError("Productivity factor must be > 0.")
            
        if self.configuration.queue_policy != "FIFO":
            raise ValueError("Only FIFO queue policy is supported.")
            
        for stage_name, stage_config in self.configuration.stages.items():
            if stage_config.base_processing_seconds <= 0:
                raise ValueError(f"Processing time must be > 0 for {stage_name}")
                
        for stage_name, workers in self.configuration.worker_config.stages_assigned.items():
            if workers < 1:
                raise ValueError(f"Worker count must be >= 1 for {stage_name}")
                
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to a deterministic dict."""
        
        stages = {}
        for k in sorted(self.configuration.stages.keys()):
            v = self.configuration.stages[k]
            stages[k] = {
                "name": v.name,
                "base_processing_seconds": v.base_processing_seconds,
                "distribution": v.distribution,
                "drivers": v.drivers,
                "description": v.description
            }
            
        config_dict = {
            "version": self.configuration.version,
            "random_seed": self.configuration.random_seed,
            "queue_policy": self.configuration.queue_policy,
            "productivity_factor": self.configuration.productivity_factor,
            "worker_config": {
                "shift_hours": self.configuration.worker_config.shift_hours,
                "stages_assigned": {k: self.configuration.worker_config.stages_assigned[k] for k in sorted(self.configuration.worker_config.stages_assigned.keys())},
                "dynamic_reallocation": self.configuration.worker_config.dynamic_reallocation
            },
            "stages": stages
        }
        
        return {
            "scenario_id": self.scenario_id,
            "scenario_name": self.scenario_name,
            "scenario_type": self.scenario_type,
            "description": self.description,
            "base_config_version": self.base_config_version,
            "model_version": self.model_version,
            "random_seed": self.random_seed,
            "parameter_changes": self.parameter_changes,
            "created_at": self.created_at,
            "configuration": config_dict
        }

    def serialize(self) -> str:
        """Deterministically serialize to JSON string."""
        d = self.to_dict()
        return json.dumps(d, sort_keys=True, separators=(',', ':'))

    def compute_hash(self) -> str:
        """Compute SHA256 hash of deterministic serialization."""
        s = self.serialize()
        return hashlib.sha256(s.encode('utf-8')).hexdigest()
        
    @staticmethod
    def load_from_dict(data: Dict[str, Any]) -> 'ScenarioDefinition':
        c_dict = data["configuration"]
        
        stages_assigned = c_dict["worker_config"]["stages_assigned"]
        shift_hours = tuple(c_dict["worker_config"]["shift_hours"])
        dynamic = c_dict["worker_config"]["dynamic_reallocation"]
        worker_config = WorkerConfiguration(stages_assigned=stages_assigned, shift_hours=shift_hours, dynamic_reallocation=dynamic)
        
        stages = {}
        for k, v in c_dict["stages"].items():
            stages[int(k)] = StageConfiguration(name=v["name"], base_processing_seconds=v["base_processing_seconds"], distribution=v["distribution"], drivers=v["drivers"], description=v["description"])
            
        config = SyntheticModelConfiguration(
            version=c_dict["version"],
            random_seed=c_dict["random_seed"],
            queue_policy=c_dict["queue_policy"],
            worker_config=worker_config,
            stages=stages,
            productivity_factor=c_dict.get("productivity_factor", 1.0)
        )
        
        return ScenarioDefinition(
            scenario_id=data["scenario_id"],
            scenario_name=data["scenario_name"],
            scenario_type=data["scenario_type"],
            description=data["description"],
            base_config_version=data["base_config_version"],
            model_version=data["model_version"],
            random_seed=data["random_seed"],
            parameter_changes=data["parameter_changes"],
            created_at=data["created_at"],
            configuration=config
        )


class ScenarioManager:
    """Manages baseline and scenario derivations."""
    def __init__(self, baseline_config: SyntheticModelConfiguration):
        self.baseline_config = baseline_config
        self.model_version = baseline_config.version
        
    def create_scenario(self, scenario_id: str, scenario_name: str, scenario_type: str, description: str, parameter_changes: Dict[str, Any]) -> ScenarioDefinition:
        """Create a scenario without mutating baseline."""
        # Deepcopy the configuration
        new_config = deepcopy(self.baseline_config)
        
        # Apply changes
        if "worker_counts" in parameter_changes:
            for stage, count in parameter_changes["worker_counts"].items():
                new_config.worker_config.stages_assigned[stage] = count
                
        if "shift_hours" in parameter_changes:
            new_config.worker_config.shift_hours = tuple(parameter_changes["shift_hours"])
            
        if "productivity_factor" in parameter_changes:
            new_config.productivity_factor = parameter_changes["productivity_factor"]
            
        if "random_seed" in parameter_changes:
            new_config.random_seed = parameter_changes["random_seed"]
            
        # Do not mutate baseline configuration!
        scenario = ScenarioDefinition(
            scenario_id=scenario_id,
            scenario_name=scenario_name,
            scenario_type=scenario_type,
            description=description,
            base_config_version=self.baseline_config.version,
            model_version=self.model_version,
            random_seed=new_config.random_seed,
            parameter_changes=parameter_changes,
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            configuration=new_config
        )
        
        scenario.validate()
        return scenario
