# Scenario Comparison & What-If Analysis Dashboard

## Purpose
The Scenario Comparison dashboard is a core module within the Streamlit visualization suite (Module 6). It is designed to provide interactive exploration and visual comparative analytics across the theoretical operational interventions (What-If scenarios) tested in the synthetic digital twin. 

It aims to answer the core analytical questions:
- *What happens to overall flow time if we add capacity to specific stages?*
- *What are the downstream unintended consequences (queue shifts) of local interventions?*
- *Which intervention yields the highest systemic ROI?*

## Data Source & Integrity
The dashboard is strictly decoupled from the heavy simulation engine (Module 5). It reads pre-aggregated, canonical analytical metrics from `data/dashboard/` generated in Module 6.1:
- `dashboard_kpis.csv`: Baseline flow and utilization summary.
- `dashboard_scenario_comparison.csv`: Pre-calculated absolute and relative deltas for each intervention scenario vs the Baseline.
- `dashboard_stage_metrics.csv`: Stage-by-stage granular queue length and utilization metrics across all scenarios.

**Important**: The dashboard does **NOT** regenerate synthetic data, modify source parameters, or alter any raw/processed datasets. It is a read-only visual overlay on verified data.

## Available Scenarios
- **Baseline**: Historical-data-anchored simulation (0% reference).
- **Dispatch +1 Worker**: Localized capacity intervention targeting the identified primary bottleneck.
- **Picking +5 Workers**: Upstream capacity intervention.
- **Packing +2 Workers**: Mid-stream capacity intervention.
- **Productivity +10%**: Theoretical global efficiency gain across all workers.
- **Extended Shift**: Process boundary intervention expanding the 10h operating window to 12h.

## KPI Definitions
- **Mean Flow Time (hrs)**: Total end-to-end time from order approval to dispatch completion.
- **P95 Flow Time (hrs)**: The 95th percentile flow time, capturing worst-case tail delays.
- **Mean Waiting Time (hrs)**: Non-value-added time orders spend in queues.
- **SLA Achievement (%)**: Percentage of orders fulfilling the 5-Day SLA constraint.
- **Improvement (%)**: The calculated reduction in Flow Time relative to the Baseline. (e.g., Extended Shift yields ~27.7% improvement).

## Dynamic Insights
The dashboard automatically parses the selected scenarios to compute:
- The intervention yielding the lowest absolute flow time.
- The intervention producing the largest percentage improvement.
- Any interventions generating negligible (<1%) systemic gains (highlighting local optima traps).

## Interpretation Limitations
- **Synthetic Outputs**: The KPIs visualized represent the outputs of the deterministic stochastic simulation. While anchored tightly to real Olist physical attributes and dates, the exact shift hours, worker assignments, and queue wait times are synthetic derivations modeling theoretical constraints.
- **Static SLA**: The 5-Day SLA is an assumed experimental parameter for monitoring, not a proven historical Olist corporate target. 
