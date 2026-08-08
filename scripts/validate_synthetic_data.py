import pandas as pd
import json
from src.synthetic.validator import SyntheticValidator
from src.synthetic.config import SyntheticModelConfiguration

def main():
    print("Loading synthetic data and configuration...")
    try:
        syn_df = pd.read_parquet("data/synthetic/synthetic_operational_data.parquet")
        orders_df = pd.read_parquet("data/processed/processed_orders.parquet")
        with open("data/synthetic/synthetic_generation_config.json", "r") as f:
            config_dict = json.load(f)
    except Exception as e:
        print(f"Error loading files: {e}")
        return
        
    validator = SyntheticValidator(syn_df, orders_df)
    
    print("Running validations...")
    struct = validator.validate_structure()
    temp = validator.validate_temporal()
    shift = validator.validate_shift()
    res = validator.validate_resources()
    
    stats = validator.calculate_statistics()
    calib = validator.analyze_calibration()
    
    scorecard = {
        "order_linkage": struct["all_orders_linked"],
        "stage_completeness": struct["exactly_five_stages"],
        "stage_continuity": temp["stage_continuity_valid"],
        "timestamp_validity": temp["end_ge_start"] and temp["end_equals_start_plus_proc"] and temp["start_after_approval"],
        "shift_compliance": shift["start_time_in_shift"],
        "worker_validity": res["worker_count_valid"],
        "queue_validity": res["queue_length_valid"],
        "processing_time_validity": temp["processing_time_valid"],
        "waiting_time_validity": temp["waiting_time_valid"],
    }
    
    overall_status = all(scorecard.values())
    
    report = {
        "status": "PASS" if overall_status else "FAIL",
        "scorecard": scorecard,
        "structural_details": struct,
        "temporal_details": temp,
        "shift_details": shift,
        "resource_details": res,
        "calibration": calib,
        "statistics": stats
    }
    
    with open("data/synthetic/synthetic_quality_report.json", "w") as f:
        json.dump(report, f, indent=4)
        
    print("\n--- SCORECARD ---")
    for k, v in scorecard.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
        
    print(f"\nOVERALL STATUS: {'PASS' if overall_status else 'FAIL'}")
    
    print("\n--- CALIBRATION ---")
    print(f"Completed before carrier: {calib['completed_before_carrier_pct']:.2f}%")
    print(f"Completed after carrier: {calib['completed_after_carrier_pct']:.2f}%")
    
if __name__ == "__main__":
    main()
