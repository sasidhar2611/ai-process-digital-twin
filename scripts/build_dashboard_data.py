import os
from src.visualization.dashboard_data import DashboardDataBuilder

def main():
    print("Building dashboard analytical datasets...")
    builder = DashboardDataBuilder(
        baseline_dir="data/results/baseline",
        scenarios_dir="data/results/scenarios",
        analysis_dir="data/results/analysis"
    )
    
    builder.save_all("data/dashboard")
    print("Dashboard datasets built successfully.")

if __name__ == "__main__":
    main()
