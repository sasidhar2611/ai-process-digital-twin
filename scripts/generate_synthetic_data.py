import pandas as pd
import json
import os
import datetime
from src.synthetic.config import SyntheticModelConfiguration
from src.synthetic.generator import SyntheticDataGenerator

def main():
    print("Loading processed data...")
    orders = pd.read_parquet("data/processed/processed_orders.parquet")
    items = pd.read_parquet("data/processed/processed_order_items.parquet")
    products = pd.read_parquet("data/processed/processed_products.parquet")
    
    config = SyntheticModelConfiguration()
    generator = SyntheticDataGenerator(config)
    
    print("Generating synthetic operational data...")
    syn_df = generator.generate(orders, products, items)
    
    os.makedirs("data/synthetic", exist_ok=True)
    
    # Save Data
    out_path = "data/synthetic/synthetic_operational_data.parquet"
    syn_df.to_parquet(out_path, index=False)
    
    # Generate Metadata
    source_orders = len(orders)
    eligible = orders[orders["eligible_for_demand_timeline"] == True] if "eligible_for_demand_timeline" in orders.columns else orders[orders["order_approved_at"].notna()]
    eligible_orders_count = len(eligible)
    generated_orders = syn_df["order_id"].nunique()
    generated_records = len(syn_df)
    
    metadata = {
        "generation_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model_version": config.version,
        "random_seed": config.random_seed,
        "source_orders": source_orders,
        "eligible_orders": eligible_orders_count,
        "generated_orders": generated_orders,
        "generated_stage_records": generated_records,
        "shift_hours": config.worker_config.shift_hours
    }
    
    with open("data/synthetic/synthetic_generation_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    with open("data/synthetic/synthetic_generation_config.json", "w") as f:
        # Convert config to dict via basic means
        config_dict = {
            "random_seed": config.random_seed,
            "version": config.version,
            "stages": {k: {"name": v.name, "base_time": v.base_processing_seconds, "drivers": v.drivers} for k, v in config.stages.items()},
            "worker_config": {
                "shift_hours": config.worker_config.shift_hours,
                "stages_assigned": config.worker_config.stages_assigned
            },
            "queue_policy": config.queue_policy
        }
        json.dump(config_dict, f, indent=4)
        
    print(f"Saved synthetic data to {out_path} ({generated_records} records).")
    
    # Calibration Report
    print("\n--- Calibration Report ---")
    print(f"Generated Orders: {generated_orders}")
    
    # Compare against carrier date
    final_stages = syn_df[syn_df["stage_sequence"] == 5]
    eval_df = final_stages.merge(orders[["order_id", "order_delivered_carrier_date"]], on="order_id", how="left")
    
    eval_df["carrier_date_valid"] = eval_df["order_delivered_carrier_date"].notna()
    valid_eval = eval_df[eval_df["carrier_date_valid"]].copy()
    
    valid_eval["completed_before_carrier"] = valid_eval["end_time"] <= valid_eval["order_delivered_carrier_date"]
    
    pct_before = (valid_eval["completed_before_carrier"].mean() * 100) if len(valid_eval) > 0 else 0
    pct_after = 100.0 - pct_before
    
    print(f"Orders with carrier dates for evaluation: {len(valid_eval)}")
    print(f"Percentage completing warehouse before carrier date: {pct_before:.2f}%")
    print(f"Percentage extending beyond carrier date: {pct_after:.2f}%")
    
    # Summary stats
    print("\n--- Distribution Report ---")
    for stage in sorted(syn_df["stage_sequence"].unique()):
        st_df = syn_df[syn_df["stage_sequence"] == stage]
        name = st_df["stage"].iloc[0]
        print(f"\nStage {stage} ({name}):")
        
        for col in ["processing_time", "waiting_time", "queue_length", "productivity_factor"]:
            s = st_df[col]
            print(f"  {col}: mean={s.mean():.2f}, p50={s.median():.2f}, p95={s.quantile(0.95):.2f}, p99={s.quantile(0.99):.2f}, min={s.min():.2f}, max={s.max():.2f}")
            
    print("\nGeneration complete.")

if __name__ == "__main__":
    main()
