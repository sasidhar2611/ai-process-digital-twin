import pytest
import pandas as pd
from src.synthetic.kpi import KPIExtractor

@pytest.fixture
def mock_df_orders():
    return pd.DataFrame({
        "order_id": ["O1", "O2"],
        "order_approved_at": [pd.Timestamp("2020-01-01 10:00:00"), pd.Timestamp("2020-01-01 11:00:00")]
    })

@pytest.fixture
def mock_df_syn():
    records = []
    
    # O1
    start = pd.Timestamp("2020-01-01 10:00:00")
    for i in range(1, 6):
        stages = {1: "PROCESSING", 2: "PICKING", 3: "PACKING", 4: "SORTING", 5: "DISPATCH"}
        proc = 100.0
        wait = 10.0
        end = start + pd.Timedelta(seconds=proc+wait)
        records.append({
            "order_id": "O1", "stage": stages[i], "stage_sequence": i,
            "start_time": start, "end_time": end,
            "processing_time": proc, "waiting_time": wait,
            "worker_count": 2, "queue_length": i
        })
        start = end
        
    # O2
    start = pd.Timestamp("2020-01-01 11:00:00")
    for i in range(1, 6):
        stages = {1: "PROCESSING", 2: "PICKING", 3: "PACKING", 4: "SORTING", 5: "DISPATCH"}
        proc = 200.0
        wait = 0.0
        end = start + pd.Timedelta(seconds=proc+wait)
        records.append({
            "order_id": "O2", "stage": stages[i], "stage_sequence": i,
            "start_time": start, "end_time": end,
            "processing_time": proc, "waiting_time": wait,
            "worker_count": 2, "queue_length": 0
        })
        start = end
        
    return pd.DataFrame(records)

def test_order_metrics(mock_df_syn, mock_df_orders):
    ext = KPIExtractor(mock_df_syn, mock_df_orders, shift_hours=(8, 18), sla_seconds=1000.0)
    order_metrics = ext.calculate_order_metrics()
    
    assert len(order_metrics) == 2
    
    # O1 total proc = 5 * 100 = 500
    # O1 total wait = 5 * 10 = 50
    # Flow time = 550
    # SLA met = 550 <= 1000 (True)
    o1 = order_metrics[order_metrics["order_id"] == "O1"].iloc[0]
    assert o1["total_processing_time"] == 500
    assert o1["total_waiting_time"] == 50
    assert o1["flow_time"] == 550
    assert o1["sla_met"] == True
    
    # O2 total proc = 1000, wait = 0
    # Flow time = 1000
    # SLA met = True
    o2 = order_metrics[order_metrics["order_id"] == "O2"].iloc[0]
    assert o2["total_processing_time"] == 1000
    assert o2["flow_time"] == 1000
    assert o2["sla_met"] == True
    
def test_stage_metrics(mock_df_syn, mock_df_orders):
    ext = KPIExtractor(mock_df_syn, mock_df_orders, shift_hours=(8, 18), sla_seconds=1000.0)
    stage_metrics = ext.calculate_stage_metrics()
    
    assert len(stage_metrics) == 5
    
    # Check processing stage
    proc_stage = stage_metrics[stage_metrics["stage"] == "PROCESSING"].iloc[0]
    assert proc_stage["orders_processed"] == 2
    # means: (100+200)/2 = 150
    assert proc_stage["mean_processing_time"] == 150.0
    # waits: (10+0)/2 = 5
    assert proc_stage["mean_waiting_time"] == 5.0
    
    # check utilization bounds
    assert 0 <= proc_stage["stage_utilization"] <= 1.0
    assert proc_stage["worker_utilization"] == proc_stage["stage_utilization"]
    
def test_generate_summary(mock_df_syn, mock_df_orders):
    ext = KPIExtractor(mock_df_syn, mock_df_orders, shift_hours=(8, 18), sla_seconds=900.0) # sla 900 so O2 fails
    order_metrics = ext.calculate_order_metrics()
    summary = ext.generate_summary("test", order_metrics)
    
    assert summary["scenario_id"] == "test"
    assert summary["orders_processed"] == 2
    assert summary["sla_breach_count"] == 1
    assert summary["sla_achievement_percentage"] == 50.0
    assert summary["mean_flow_time"] == 775.0 # (550 + 1000) / 2
