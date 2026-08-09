import pandas as pd
import streamlit as st
import os
from app.config import (
    KPI_DATA_PATH, STAGE_METRICS_PATH, SCENARIO_COMP_PATH,
    INTERVENTION_RANKING_PATH, BOTTLENECK_SUMMARY_PATH
)

@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dashboard dataset not found at {path}. Please run Module 6.1 first.")
    try:
        df = pd.read_csv(path)
        if df.empty:
            raise ValueError(f"Dataset {path} is empty.")
        return df
    except Exception as e:
        raise ValueError(f"Error loading {path}: {e}")

def load_kpis():
    return load_csv(KPI_DATA_PATH)

def load_stage_metrics():
    return load_csv(STAGE_METRICS_PATH)

def load_scenario_comparison():
    return load_csv(SCENARIO_COMP_PATH)

def load_intervention_ranking():
    return load_csv(INTERVENTION_RANKING_PATH)

def load_bottleneck_summary():
    return load_csv(BOTTLENECK_SUMMARY_PATH)
