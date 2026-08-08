import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.processed_dataset_builder import ProcessedDatasetBuilder

def run_build():
    print("Building processed datasets...")
    builder = ProcessedDatasetBuilder()
    results = builder.build_all()
    
    with open("processed_data_quality_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("Build complete. Output written to data/processed/")
    
if __name__ == "__main__":
    run_build()
