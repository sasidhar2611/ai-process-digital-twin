from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class StageConfiguration:
    name: str
    base_processing_seconds: float
    distribution: str
    drivers: List[str]
    description: str
    
@dataclass
class WorkerConfiguration:
    shift_hours: tuple = (8, 18) # 8 AM to 6 PM
    stages_assigned: Dict[str, int] = field(default_factory=lambda: {
        "PROCESSING": 5,
        "PICKING": 15,
        "PACKING": 10,
        "SORTING": 5,
        "DISPATCH": 3
    })
    dynamic_reallocation: bool = False

@dataclass
class SyntheticModelConfiguration:
    """
    Configuration for reproducible synthetic operational data generation.
    """
    random_seed: int = 42
    version: str = "1.0.0"
    
    stages: Dict[int, StageConfiguration] = field(default_factory=lambda: {
        1: StageConfiguration("PROCESSING", 60.0, "lognormal", ["order_status"], "Initial digital routing/processing"),
        2: StageConfiguration("PICKING", 300.0, "lognormal", ["item_count", "total_volume_cm3"], "Physical picking in warehouse"),
        3: StageConfiguration("PACKING", 120.0, "lognormal", ["item_count", "total_weight_g"], "Packing into boxes"),
        4: StageConfiguration("SORTING", 45.0, "lognormal", ["customer_state"], "Sorting by carrier route"),
        5: StageConfiguration("DISPATCH", 180.0, "lognormal", ["total_weight_g"], "Loading onto carrier")
    })
    
    worker_config: WorkerConfiguration = field(default_factory=WorkerConfiguration)
    queue_policy: str = "FIFO"
