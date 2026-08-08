import pytest
import pandas as pd
import numpy as np
from src.synthetic.config import SyntheticModelConfiguration, WorkerConfiguration, StageConfiguration
from src.synthetic.generator import SyntheticDataGenerator

@pytest.fixture
def sample_orders():
    return pd.DataFrame({
        "order_id": ["O1", "O2", "O3"],
        "order_approved_at": [
            pd.Timestamp("2020-01-01 10:00:00"),
            pd.Timestamp("2020-01-01 19:00:00"), # out of shift
            pd.Timestamp("2020-01-02 08:30:00")
        ],
        "eligible_for_demand_timeline": [True, True, True],
        "customer_state": ["SP", "RJ", "MG"]
    })

@pytest.fixture
def sample_items():
    return pd.DataFrame({
        "order_id": ["O1", "O1", "O2", "O3"],
        "product_id": ["P1", "P2", "P1", "P3"]
    })

@pytest.fixture
def sample_products():
    return pd.DataFrame({
        "product_id": ["P1", "P2", "P3"],
        "product_weight_g": [500, 1500, 200],
        "physical_volume_cm3": [1000, 3000, 500]
    })

def test_shift_handling(sample_orders):
    config = SyntheticModelConfiguration()
    gen = SyntheticDataGenerator(config)
    
    # 10:00 is during shift, should remain unchanged
    t1 = pd.Timestamp("2020-01-01 10:00:00")
    assert gen._next_working_time(t1) == t1
    
    # 19:00 is after shift, should move to next day 08:00
    t2 = pd.Timestamp("2020-01-01 19:00:00")
    assert gen._next_working_time(t2) == pd.Timestamp("2020-01-02 08:00:00")
    
    # 07:00 is before shift, should move to today 08:00
    t3 = pd.Timestamp("2020-01-01 07:00:00")
    assert gen._next_working_time(t3) == pd.Timestamp("2020-01-01 08:00:00")

def test_generation_basics(sample_orders, sample_items, sample_products):
    config = SyntheticModelConfiguration(random_seed=42)
    gen = SyntheticDataGenerator(config)
    
    df_syn = gen.generate(sample_orders, sample_products, sample_items)
    
    # 3 orders * 5 stages = 15 records
    assert len(df_syn) == 15
    
    # Sequence check
    for order_id, group in df_syn.groupby("order_id"):
        assert len(group) == 5
        assert list(group["stage_sequence"]) == [1, 2, 3, 4, 5]
        
        # Chronology
        start_times = group["start_time"].values
        end_times = group["end_time"].values
        for i in range(5):
            assert start_times[i] <= end_times[i]
            assert group["processing_time"].iloc[i] > 0
            assert group["waiting_time"].iloc[i] >= 0
            
            if i > 0:
                assert start_times[i] >= end_times[i-1]

def test_determinism(sample_orders):
    config1 = SyntheticModelConfiguration(random_seed=123)
    gen1 = SyntheticDataGenerator(config1)
    df1 = gen1.generate(sample_orders)
    
    config2 = SyntheticModelConfiguration(random_seed=123)
    gen2 = SyntheticDataGenerator(config2)
    df2 = gen2.generate(sample_orders)
    
    pd.testing.assert_frame_equal(df1, df2)
