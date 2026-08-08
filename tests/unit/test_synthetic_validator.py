import pytest
import pandas as pd
from src.synthetic.validator import SyntheticValidator

@pytest.fixture
def mock_df_orders():
    return pd.DataFrame({
        "order_id": ["O1", "O2"],
        "order_approved_at": [pd.Timestamp("2020-01-01 10:00:00"), pd.Timestamp("2020-01-01 11:00:00")]
    })

@pytest.fixture
def mock_df_syn():
    # Provide a perfect valid dataframe for O1
    records = []
    start = pd.Timestamp("2020-01-01 10:00:00")
    for i in range(1, 6):
        stages = {1: "PROCESSING", 2: "PICKING", 3: "PACKING", 4: "SORTING", 5: "DISPATCH"}
        proc_time = 100.0
        end = start + pd.Timedelta(seconds=proc_time)
        records.append({
            "order_id": "O1",
            "stage": stages[i],
            "stage_sequence": i,
            "start_time": start,
            "end_time": end,
            "processing_time": proc_time,
            "waiting_time": 0.0,
            "worker_id": 1,
            "worker_count": 2,
            "productivity_factor": 1.0,
            "queue_length": 0,
            "item_count": 1,
            "total_weight_g": 100,
            "total_volume_cm3": 100
        })
        start = end
        
    # Same for O2
    start2 = pd.Timestamp("2020-01-01 11:00:00")
    for i in range(1, 6):
        stages = {1: "PROCESSING", 2: "PICKING", 3: "PACKING", 4: "SORTING", 5: "DISPATCH"}
        proc_time = 150.0
        end2 = start2 + pd.Timedelta(seconds=proc_time)
        records.append({
            "order_id": "O2",
            "stage": stages[i],
            "stage_sequence": i,
            "start_time": start2,
            "end_time": end2,
            "processing_time": proc_time,
            "waiting_time": 0.0,
            "worker_id": 1,
            "worker_count": 2,
            "productivity_factor": 1.0,
            "queue_length": 0,
            "item_count": 1,
            "total_weight_g": 100,
            "total_volume_cm3": 100
        })
        start2 = end2
        
    return pd.DataFrame(records)

def test_structural_validation(mock_df_syn, mock_df_orders):
    validator = SyntheticValidator(mock_df_syn, mock_df_orders)
    res = validator.validate_structure()
    assert res["all_orders_linked"]
    assert res["exactly_five_stages"]
    assert res["sequence_valid"]
    assert res["names_valid"]

def test_temporal_validation(mock_df_syn, mock_df_orders):
    validator = SyntheticValidator(mock_df_syn, mock_df_orders)
    res = validator.validate_temporal()
    assert res["processing_time_valid"]
    assert res["waiting_time_valid"]
    assert res["end_ge_start"]
    assert res["end_equals_start_plus_proc"]
    assert res["stage_continuity_valid"]
    assert res["start_after_approval"]

def test_shift_validation(mock_df_syn, mock_df_orders):
    validator = SyntheticValidator(mock_df_syn, mock_df_orders)
    res = validator.validate_shift(8, 18)
    assert res["start_time_in_shift"]

def test_resource_validation(mock_df_syn, mock_df_orders):
    validator = SyntheticValidator(mock_df_syn, mock_df_orders)
    res = validator.validate_resources()
    assert res["worker_count_valid"]
    assert res["queue_length_valid"]
    assert res["productivity_valid"]
