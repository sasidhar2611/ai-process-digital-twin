from enum import Enum, IntEnum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

class ProcessStage(IntEnum):
    """
    Defines the exact stages and their sequence in the fulfillment process.
    """
    PROCESSING = 1
    PICKING = 2
    PACKING = 3
    SORTING = 4
    DISPATCH = 5

@dataclass
class SyntheticFieldDefinition:
    name: str
    dtype: str
    is_real: bool
    is_derived: bool
    is_synthetic: bool
    is_assumption: bool
    description: str

@dataclass
class OperationalSchema:
    """
    Defines the exact schema for the future synthetic operational dataset.
    """
    fields: List[SyntheticFieldDefinition] = field(default_factory=lambda: [
        # Linkage
        SyntheticFieldDefinition("order_id", "string", True, False, False, False, "REAL: Foreign key to Olist orders"),
        SyntheticFieldDefinition("item_count", "int64", False, True, False, False, "DERIVED: Number of items in the order"),
        SyntheticFieldDefinition("total_weight_g", "float64", False, True, False, False, "DERIVED: Total weight of items"),
        SyntheticFieldDefinition("total_volume_cm3", "float64", False, True, False, False, "DERIVED: Total volume of items"),
        
        # Operational
        SyntheticFieldDefinition("stage", "string", False, False, True, False, "SYNTHETIC: Name of the process stage"),
        SyntheticFieldDefinition("stage_sequence", "int64", False, False, True, True, "ASSUMPTION: The integer sequence of the stage"),
        SyntheticFieldDefinition("start_time", "datetime64[us]", False, False, True, True, "ASSUMPTION: When the stage begins"),
        SyntheticFieldDefinition("end_time", "datetime64[us]", False, False, True, True, "ASSUMPTION: When the stage completes"),
        SyntheticFieldDefinition("processing_time", "float64", False, False, True, True, "ASSUMPTION: Active processing time in seconds"),
        SyntheticFieldDefinition("waiting_time", "float64", False, False, True, True, "ASSUMPTION: Time spent waiting in queue in seconds"),
        
        # Resources
        SyntheticFieldDefinition("worker_id", "int64", False, False, True, True, "ASSUMPTION: ID of the synthetic worker assigned"),
        SyntheticFieldDefinition("worker_count", "int64", False, False, True, True, "ASSUMPTION: Number of workers simultaneously assigned"),
        SyntheticFieldDefinition("productivity_factor", "float64", False, False, True, True, "ASSUMPTION: Speed multiplier of the assigned worker(s)"),
        SyntheticFieldDefinition("queue_length", "int64", False, False, True, True, "ASSUMPTION: Items waiting at the moment processing starts")
    ])

    def get_field_names(self) -> List[str]:
        return [f.name for f in self.fields]
