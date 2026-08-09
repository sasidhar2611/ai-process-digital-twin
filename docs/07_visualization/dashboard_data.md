# Dashboard Data Preparation

## 1. Purpose
This document outlines the extraction and preparation of a compact analytical dataset layer designed specifically for consumption by dashboard visualization tools (e.g., Streamlit, Power BI, KNIME). 

The goal is to flatten complex nested JSONs and heavy Parquet files into lightweight, portable CSVs containing only the metrics needed for interactive visual analysis, preventing visualization tools from needing to process the raw 99,000+ row operational event logs.

## 2. Source Datasets (Data Provenance)
No new operational data was generated in this step. All dashboard data is directly extracted, transformed, and loaded (ETL) from the existing canonical analytical outputs produced in Module 5:
- `data/results/baseline/baseline_kpis.json`
- `data/results/baseline/baseline_stage_metrics.parquet`
- `data/results/scenarios/*/`
- `data/results/analysis/bottleneck_analysis.json`
- `data/results/analysis/intervention_ranking.json`

## 3. Transformations & Conversions
- **Scenario Labeling**: Raw scenario IDs (e.g., `dispatch_plus_1`) were mapped to human-readable labels (`Dispatch +1 Worker`).
- **Unit Conversions**: Added explicit hours conversions (e.g., `mean_flow_time_hours`) where useful for executive-level charts, without dropping the original seconds-based measurements (`mean_flow_time_seconds`).
- **Flattening**: Ranked JSON arrays were flattened into tabular rows. Stage metrics were stacked into a single consolidated table with explicit scenario labels.

## 4. Output Datasets

All outputs are saved as `.csv` in `data/dashboard/`.

### 4.1 dashboard_kpis.csv
Contains the primary executive-level KPI cards for all scenarios.
- **Columns**: `scenario`, `scenario_label`, `orders_processed`, `mean_flow_time_seconds`, `mean_flow_time_hours`, `median_flow_time_seconds`, `p95_flow_time_seconds`, `p99_flow_time_seconds`, `mean_processing_time_seconds`, `mean_waiting_time_seconds`, `mean_waiting_time_hours`, `sla_achievement_percent`, `sla_breach_count`

### 4.2 dashboard_stage_metrics.csv
Contains metrics mapped directly to the 5 individual warehouse stages. Used for bottleneck and utilization charts.
- **Columns**: `scenario`, `scenario_label`, `stage`, `stage_sequence`, `worker_count`, `utilization_percent`, `mean_queue`, `p95_queue`, `max_queue`, `mean_processing_time_seconds`, `mean_waiting_time_seconds`

### 4.3 dashboard_scenario_comparison.csv
Contains direct delta comparisons between the what-if scenarios and the baseline.
- **Columns**: `scenario`, `scenario_label`, `scenario_type`, `description`, `mean_flow_time_seconds`, `mean_flow_time_change_seconds`, `mean_flow_time_change_percent`, `p95_flow_time_seconds`, `p95_flow_time_change_percent`, `mean_waiting_time_seconds`, `mean_waiting_time_change_seconds`, `mean_waiting_time_change_percent`, `sla_achievement_percent`, `hypothesis_result`

### 4.4 dashboard_intervention_ranking.csv
Contains the formalized ranking of interventions produced by Module 5.7.
- **Columns**: `rank`, `scenario`, `scenario_label`, `intervention_category`, `mean_flow_time_improvement_percent`, `mean_waiting_time_improvement_percent`, `p95_flow_time_improvement_percent`, `bottleneck_effect`, `hypothesis_result`, `recommendation_priority`

### 4.5 dashboard_bottleneck_summary.csv
Contains the formalized bottleneck scoring methodology for the baseline state.
- **Columns**: `stage`, `utilization_percent`, `mean_queue`, `p95_queue`, `mean_waiting_time_seconds`, `bottleneck_score`, `bottleneck_rank`, `bottleneck_role`

## 5. Validation
The dashboard build pipeline includes automated unit tests ensuring:
1. Scenario counts (6) and Stage counts (5) match exactly.
2. Value mappings are consistent and column names exist.
3. No operational data is simulated during the extraction process (guaranteeing deterministic outputs matching prior module findings).

## 6. Intended Consumers
- Streamlit application (Upcoming Phase).
- External BI Analysts via Power BI or Tableau loading the `data/dashboard/` CSVs.
