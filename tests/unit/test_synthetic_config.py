import pytest
from src.synthetic.schema import ProcessStage, OperationalSchema
from src.synthetic.config import SyntheticModelConfiguration, WorkerConfiguration, StageConfiguration

def test_process_stage_enum():
    assert ProcessStage.PROCESSING == 1
    assert ProcessStage.PICKING == 2
    assert ProcessStage.PACKING == 3
    assert ProcessStage.SORTING == 4
    assert ProcessStage.DISPATCH == 5
    
def test_operational_schema():
    schema = OperationalSchema()
    fields = schema.get_field_names()
    
    # Real/Derived fields
    assert "order_id" in fields
    assert "item_count" in fields
    assert "total_weight_g" in fields
    assert "total_volume_cm3" in fields
    
    # Synthetic operational fields
    assert "stage" in fields
    assert "stage_sequence" in fields
    assert "start_time" in fields
    assert "end_time" in fields
    assert "processing_time" in fields
    assert "waiting_time" in fields
    assert "worker_id" in fields
    assert "worker_count" in fields
    assert "productivity_factor" in fields
    assert "queue_length" in fields
    
    # Check that Real/Derived/Synthetic constraints exist correctly
    for field in schema.fields:
        if field.name == "order_id":
            assert field.is_real is True
            assert field.is_synthetic is False
        elif field.name == "item_count":
            assert field.is_derived is True
            assert field.is_synthetic is False
        elif field.name == "stage":
            assert field.is_synthetic is True
            assert field.is_real is False
            assert field.is_assumption is False # Explicit outcome, not assumption
        elif field.name == "processing_time":
            assert field.is_synthetic is True
            assert field.is_assumption is True

def test_synthetic_config_defaults():
    config = SyntheticModelConfiguration()
    assert config.random_seed == 42
    assert config.queue_policy == "FIFO"
    assert not config.worker_config.dynamic_reallocation
    
    # Validate stages exist
    assert 1 in config.stages
    assert config.stages[1].name == "PROCESSING"
    assert config.stages[5].name == "DISPATCH"
