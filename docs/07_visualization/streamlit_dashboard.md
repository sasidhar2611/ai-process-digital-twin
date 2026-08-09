# Streamlit Dashboard Foundation

## Purpose
This module provides the frontend visualization layer for the AI-Process-Digital-Twin project. It consumes the pre-computed dashboard datasets (CSV files) to render an interactive overview of the warehouse digital twin performance.

## Architecture
The application is built using **Streamlit** for the frontend UI and **Plotly** for visualizations. It strictly avoids re-running the synthetic generator or connecting to heavy Parquet files, instead relying entirely on the `data/dashboard/*.csv` layer.

## Entry Point
The application entry point is `app/streamlit_app.py`.

## Data Sources
- `data/dashboard/dashboard_kpis.csv`
- `data/dashboard/dashboard_stage_metrics.csv`
- `data/dashboard/dashboard_scenario_comparison.csv`
- `data/dashboard/dashboard_intervention_ranking.csv`
- `data/dashboard/dashboard_bottleneck_summary.csv`

## Page Structure
Currently implemented:
- **Overview**: Displays baseline KPIs (Flow Time, Waiting Time), bottleneck summary, and visualizations for stage utilization and queue lengths.

Future planned pages:
- **Bottleneck Analysis**: Detailed exploration of bottlenecks.
- **What-If Analysis**: Scenario comparison metrics.
- **Intervention Ranking**: Formal intervention evaluation.

## Error Handling
The application uses robust `try/except` blocks in the loading layer (`app/data_loader.py`) to catch missing or malformed CSV files and displays user-friendly `st.error` messages instead of raw Python stack traces.

## Limitations
- Does not contain real-time updates.
- Strictly offline, presenting the results of the previously run simulations.
- Assumes the pre-computation pipeline (Module 6.1) has been executed successfully.

## How to Run Locally
Run the following command from the project root:
```bash
streamlit run app/streamlit_app.py
```
