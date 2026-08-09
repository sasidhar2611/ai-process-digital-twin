import pytest
from app.data_loader import (
    load_kpis,
    load_stage_metrics,
    load_scenario_comparison,
    load_intervention_ranking,
    load_bottleneck_summary,
    load_csv
)
from app import config
import os

def test_data_paths():
    assert os.path.join("data", "dashboard") in config.DASHBOARD_DATA_DIR
    assert "dashboard_kpis.csv" in config.KPI_DATA_PATH

def test_load_kpis():
    df = load_kpis()
    assert not df.empty
    assert "scenario" in df.columns
    assert "orders_processed" in df.columns
    
    # baseline exists
    assert "baseline" in df["scenario"].values

def test_load_stage_metrics():
    df = load_stage_metrics()
    assert not df.empty
    assert "stage_sequence" in df.columns
    
def test_load_bottleneck_summary():
    df = load_bottleneck_summary()
    assert not df.empty
    assert "bottleneck_score" in df.columns

def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("non_existent_file.csv")

def test_load_csv_empty_handling(tmp_path):
    empty_file = os.path.join(tmp_path, "empty.csv")
    with open(empty_file, "w") as f:
        f.write("")
    
    with pytest.raises(ValueError, match="Error loading"):
        load_csv(empty_file)
