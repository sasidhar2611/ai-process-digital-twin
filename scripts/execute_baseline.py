import pandas as pd
import json
import os
import datetime
from src.synthetic.kpi import KPIExtractor

def main():
    print("Loading data...")
    try:
        # Load Baseline config
        with open("config/scenarios/baseline.json", "r") as f:
            baseline_config = json.load(f)
            
        # Load synthetic data
        syn_df = pd.read_parquet("data/synthetic/synthetic_operational_data.parquet")
        orders_df = pd.read_parquet("data/processed/processed_orders.parquet")
    except Exception as e:
        print(f"Error loading files: {e}")
        return
        
    print("Extracting KPIs for baseline scenario...")
    
    # SLA 5 days in seconds
    sla_seconds = 5 * 24 * 3600.0
    shift_hours = tuple(baseline_config["configuration"]["worker_config"]["shift_hours"])
    
    extractor = KPIExtractor(syn_df, orders_df, shift_hours=shift_hours, sla_seconds=sla_seconds)
    
    # Order Level Metrics
    order_metrics = extractor.calculate_order_metrics()
    
    # Stage Level Metrics
    stage_metrics = extractor.calculate_stage_metrics()
    
    # Summary
    summary = extractor.generate_summary("baseline", order_metrics)
    
    # Data Provenance & Metadata
    metadata = {
        "scenario_id": "baseline",
        "model_version": baseline_config["model_version"],
        "configuration_version": baseline_config["base_config_version"],
        "random_seed": baseline_config["random_seed"],
        "source_data_reference": "data/processed/",
        "execution_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sla_definition_seconds": sla_seconds
    }
    
    # Save outputs
    os.makedirs("data/results/baseline", exist_ok=True)
    
    order_metrics.to_parquet("data/results/baseline/baseline_order_metrics.parquet", index=False)
    stage_metrics.to_parquet("data/results/baseline/baseline_stage_metrics.parquet", index=False)
    
    with open("data/results/baseline/baseline_kpis.json", "w") as f:
        json.dump(summary, f, indent=4)
        
    with open("data/results/baseline/baseline_execution_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Baseline execution completed successfully.")
    print("\n--- BASELINE SUMMARY ---")
    for k, v in summary.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
