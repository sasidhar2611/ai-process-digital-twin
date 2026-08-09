import pandas as pd
import json
from typing import Dict, Any, List

class BottleneckAnalyzer:
    def __init__(self, baseline_stage_metrics_path: str, baseline_kpis_path: str):
        self.stage_metrics = pd.read_parquet(baseline_stage_metrics_path)
        with open(baseline_kpis_path, 'r') as f:
            self.baseline_kpis = json.load(f)
            
    def compute_bottleneck_scores(self) -> pd.DataFrame:
        """
        Computes transparent bottleneck scores for each stage.
        Methodology:
        For each stage, we normalize four critical metrics against the maximum observed value across all stages:
        1. Stage Utilization
        2. Mean Queue Length
        3. P95 Queue Length
        4. Mean Waiting Time
        
        Normalized Metric = Stage Value / Max Value across all stages (so the worst stage gets 1.0)
        Total Score = Sum of the 4 normalized metrics (Max possible = 4.0).
        """
        df = self.stage_metrics.copy()
        
        metrics = [
            'stage_utilization',
            'mean_queue_length',
            'p95_queue_length',
            'mean_waiting_time'
        ]
        
        for m in metrics:
            max_val = df[m].max()
            if max_val > 0:
                df[f'{m}_norm'] = df[m] / max_val
            else:
                df[f'{m}_norm'] = 0.0
                
        df['bottleneck_score'] = df[[f'{m}_norm' for m in metrics]].sum(axis=1)
        return df.sort_values('bottleneck_score', ascending=False)
        
    def analyze_baseline(self) -> Dict[str, Any]:
        scored_df = self.compute_bottleneck_scores()
        
        highest_util = scored_df.loc[scored_df['stage_utilization'].idxmax()]
        highest_queue = scored_df.loc[scored_df['mean_queue_length'].idxmax()]
        highest_wait = scored_df.loc[scored_df['mean_waiting_time'].idxmax()]
        overall_bottleneck = scored_df.iloc[0]
        
        return {
            "highest_utilization_stage": highest_util['stage'],
            "highest_queue_stage": highest_queue['stage'],
            "largest_waiting_contribution_stage": highest_wait['stage'],
            "overall_bottleneck_candidate": overall_bottleneck['stage'],
            "stage_scores": scored_df[['stage', 'stage_utilization', 'mean_queue_length', 'mean_waiting_time', 'bottleneck_score']].to_dict(orient='records')
        }

class InterventionRanker:
    def __init__(self, baseline_kpis_path: str, scenarios_kpis_paths: Dict[str, str]):
        with open(baseline_kpis_path, 'r') as f:
            self.baseline_kpis = json.load(f)
            
        self.scenarios = {}
        for name, path in scenarios_kpis_paths.items():
            with open(path, 'r') as f:
                self.scenarios[name] = json.load(f)
                
    def rank_interventions(self) -> List[Dict[str, Any]]:
        results = []
        b_flow = self.baseline_kpis['mean_flow_time']
        b_p95_flow = self.baseline_kpis['p95_flow_time']
        b_wait = self.baseline_kpis['mean_waiting_time']
        
        for name, kpis in self.scenarios.items():
            s_flow = kpis['mean_flow_time']
            s_p95_flow = kpis['p95_flow_time']
            s_wait = kpis['mean_waiting_time']
            
            flow_imp = b_flow - s_flow
            p95_flow_imp = b_p95_flow - s_p95_flow
            wait_imp = b_wait - s_wait
            
            results.append({
                "scenario": name,
                "mean_flow_time_improvement_s": flow_imp,
                "p95_flow_time_improvement_s": p95_flow_imp,
                "mean_waiting_time_improvement_s": wait_imp,
                "mean_flow_time_improvement_pct": (flow_imp / b_flow) * 100 if b_flow > 0 else 0,
            })
            
        # Rank primarily by mean flow time improvement (descending)
        results.sort(key=lambda x: x['mean_flow_time_improvement_s'], reverse=True)
        return results
