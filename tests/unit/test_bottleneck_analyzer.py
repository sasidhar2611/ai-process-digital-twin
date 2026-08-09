import pytest
import pandas as pd
import json
import os
from unittest.mock import patch, mock_open
from src.analysis.bottleneck_analyzer import BottleneckAnalyzer, InterventionRanker

@pytest.fixture
def mock_stage_metrics():
    return pd.DataFrame({
        'stage': ['PROCESSING', 'PICKING', 'PACKING', 'SORTING', 'DISPATCH'],
        'stage_utilization': [0.1, 0.2, 0.05, 0.02, 0.5],
        'mean_queue_length': [10.0, 5.0, 0.1, 0.1, 40.0],
        'p95_queue_length': [20.0, 10.0, 0.5, 0.2, 80.0],
        'mean_waiting_time': [5000.0, 2000.0, 100.0, 50.0, 10000.0]
    })

@pytest.fixture
def mock_kpis():
    return json.dumps({
        'mean_flow_time': 20000.0,
        'p95_flow_time': 50000.0,
        'mean_waiting_time': 18000.0
    })

@pytest.fixture
def mock_scenario_kpis():
    return json.dumps({
        'mean_flow_time': 18000.0,
        'p95_flow_time': 45000.0,
        'mean_waiting_time': 16000.0
    })

def test_bottleneck_scoring(mock_stage_metrics, mock_kpis):
    with patch('pandas.read_parquet', return_value=mock_stage_metrics), \
         patch('builtins.open', mock_open(read_data=mock_kpis)):
        
        analyzer = BottleneckAnalyzer("dummy.parquet", "dummy.json")
        scores = analyzer.compute_bottleneck_scores()
        
        assert len(scores) == 5
        # Dispatch should have the highest score as it has highest in all metrics
        assert scores.iloc[0]['stage'] == 'DISPATCH'
        assert scores.iloc[0]['bottleneck_score'] == 4.0 # max score

def test_analyze_baseline_results(mock_stage_metrics, mock_kpis):
    with patch('pandas.read_parquet', return_value=mock_stage_metrics), \
         patch('builtins.open', mock_open(read_data=mock_kpis)):
        
        analyzer = BottleneckAnalyzer("dummy.parquet", "dummy.json")
        result = analyzer.analyze_baseline()
        
        assert result['highest_utilization_stage'] == 'DISPATCH'
        assert result['highest_queue_stage'] == 'DISPATCH'
        assert result['overall_bottleneck_candidate'] == 'DISPATCH'

def test_intervention_ranking(mock_kpis, mock_scenario_kpis):
    with patch('builtins.open') as m_open:
        m_open.side_effect = [
            mock_open(read_data=mock_kpis).return_value,
            mock_open(read_data=mock_scenario_kpis).return_value
        ]
        
        ranker = InterventionRanker("dummy.json", {"test_scenario": "dummy2.json"})
        ranking = ranker.rank_interventions()
        
        assert len(ranking) == 1
        assert ranking[0]['scenario'] == 'test_scenario'
        assert ranking[0]['mean_flow_time_improvement_s'] == 2000.0
        assert ranking[0]['mean_flow_time_improvement_pct'] == 10.0
