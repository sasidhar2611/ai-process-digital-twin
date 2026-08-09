import pandas as pd
import json
import os
import datetime
from src.synthetic.scenario import ScenarioDefinition
from src.synthetic.generator import SyntheticDataGenerator
from src.synthetic.kpi import KPIExtractor

def main():
    print("Loading data...")
    try:
        # Load Dispatch+1 config
        with open("config/scenarios/dispatch_plus_1.json", "r") as f:
            scenario_data = json.load(f)
            scenario = ScenarioDefinition.load_from_dict(scenario_data)
            
        # Load synthetic data dependencies
        orders_df = pd.read_parquet("data/processed/processed_orders.parquet")
        items_df = pd.read_parquet("data/processed/processed_order_items.parquet")
        products_df = pd.read_parquet("data/processed/processed_products.parquet")
    except Exception as e:
        print(f"Error loading files: {e}")
        return
        
    print("Executing Dispatch +1 simulation...")
    
    # Run simulation 1
    generator1 = SyntheticDataGenerator(scenario.configuration)
    syn_df1 = generator1.generate(orders_df, products_df, items_df)
    
    # Run simulation 2 for reproducibility check
    print("Executing Dispatch +1 simulation (run 2) for determinism check...")
    generator2 = SyntheticDataGenerator(scenario.configuration)
    syn_df2 = generator2.generate(orders_df, products_df, items_df)
    
    if syn_df1.equals(syn_df2):
        print("DETERMINISM CHECK: PASS - Both runs produced identical results.")
    else:
        print("DETERMINISM CHECK: FAIL - Runs produced different results.")
        return
        
    syn_df = syn_df1
        
    print("Extracting KPIs for Dispatch +1 scenario...")
    
    sla_seconds = 5 * 24 * 3600.0
    shift_hours = tuple(scenario.configuration.worker_config.shift_hours)
    
    extractor = KPIExtractor(syn_df, orders_df, shift_hours=shift_hours, sla_seconds=sla_seconds)
    
    order_metrics = extractor.calculate_order_metrics()
    stage_metrics = extractor.calculate_stage_metrics()
    summary = extractor.generate_summary("dispatch_plus_1", order_metrics)
    
    metadata = {
        "scenario_id": "dispatch_plus_1",
        "model_version": scenario.model_version,
        "configuration_version": scenario.base_config_version,
        "random_seed": scenario.random_seed,
        "source_data_reference": "data/processed/",
        "execution_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sla_definition_seconds": sla_seconds
    }
    
    os.makedirs("data/results/scenarios/dispatch_plus_1", exist_ok=True)
    
    order_metrics.to_parquet("data/results/scenarios/dispatch_plus_1/dispatch_plus_1_order_metrics.parquet", index=False)
    stage_metrics.to_parquet("data/results/scenarios/dispatch_plus_1/dispatch_plus_1_stage_metrics.parquet", index=False)
    
    with open("data/results/scenarios/dispatch_plus_1/dispatch_plus_1_kpis.json", "w") as f:
        json.dump(summary, f, indent=4)
        
    with open("data/results/scenarios/dispatch_plus_1/dispatch_plus_1_execution_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    # Load Baseline
    print("Comparing with Baseline...")
    with open("data/results/baseline/baseline_kpis.json", "r") as f:
        baseline_summary = json.load(f)
        
    comparison = {}
    for k in baseline_summary.keys():
        val_b = baseline_summary[k]
        val_d = summary[k]
        
        if isinstance(val_b, (int, float)) and not isinstance(val_b, bool):
            abs_change = val_d - val_b
            pct_change = (abs_change / val_b * 100) if val_b != 0 else 0
            
            comparison[k] = {
                "baseline": val_b,
                "dispatch_plus_1": val_d,
                "absolute_change": abs_change,
                "percentage_change": pct_change
            }
        else:
            comparison[k] = {
                "baseline": val_b,
                "dispatch_plus_1": val_d
            }
        
    with open("data/results/scenarios/baseline_vs_dispatch_plus_1.json", "w") as f:
        json.dump(comparison, f, indent=4)
        
    print("Scenario execution and comparison completed successfully.")
    
if __name__ == "__main__":
    main()
