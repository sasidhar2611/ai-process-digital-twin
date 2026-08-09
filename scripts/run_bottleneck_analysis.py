import os
import json
from src.analysis.bottleneck_analyzer import BottleneckAnalyzer, InterventionRanker

def main():
    print("Running Formal Bottleneck Analysis & Intervention Ranking...")
    
    baseline_stage_metrics = "data/results/baseline/baseline_stage_metrics.parquet"
    baseline_kpis = "data/results/baseline/baseline_kpis.json"
    
    scenarios = {
        "dispatch_plus_1": "data/results/scenarios/dispatch_plus_1/dispatch_plus_1_kpis.json",
        "picking_plus_5": "data/results/scenarios/picking_plus_5/picking_plus_5_kpis.json",
        "packing_plus_2": "data/results/scenarios/packing_plus_2/packing_plus_2_kpis.json",
        "productivity_plus_10": "data/results/scenarios/productivity_plus_10/productivity_plus_10_kpis.json",
        "extended_shift": "data/results/scenarios/extended_shift/extended_shift_kpis.json"
    }
    
    os.makedirs("data/results/analysis", exist_ok=True)
    
    # 1. Bottleneck Analysis
    analyzer = BottleneckAnalyzer(baseline_stage_metrics, baseline_kpis)
    bottleneck_results = analyzer.analyze_baseline()
    
    with open("data/results/analysis/bottleneck_analysis.json", "w") as f:
        json.dump(bottleneck_results, f, indent=4)
        
    print(f"Baseline Bottleneck: {bottleneck_results['overall_bottleneck_candidate']}")
    
    # 2. Intervention Ranking
    ranker = InterventionRanker(baseline_kpis, scenarios)
    ranking = ranker.rank_interventions()
    
    with open("data/results/analysis/intervention_ranking.json", "w") as f:
        json.dump({"ranking": ranking}, f, indent=4)
        
    print("Ranking complete. Top intervention:")
    print(f"{ranking[0]['scenario']} with {ranking[0]['mean_flow_time_improvement_pct']:.2f}% improvement")

if __name__ == "__main__":
    main()
