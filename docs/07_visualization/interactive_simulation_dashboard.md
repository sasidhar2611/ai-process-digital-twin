# Interactive What-If Simulation Dashboard

## Purpose
The Interactive What-If Simulation dashboard (Module 6.6) allows users to explore theoretical operational changes to the warehouse fulfillment process. It compares the canonical baseline against a predefined set of tested operational interventions.

## Data Source & Integrity
To preserve extreme UI responsiveness and maintain deterministic reproducibility, this dashboard strictly relies on pre-computed simulation outputs from Module 5.6 (`data/dashboard/dashboard_scenario_comparison.csv` and `data/dashboard/dashboard_stage_metrics.csv`).

**CRITICAL CONSTRAINT**: The dashboard does **NOT** regenerate synthetic operational data nor does it run a live simulation engine behind the scenes. It merely overlays existing, validated scenario results. This distinction is clearly communicated in the UI to prevent misrepresenting the application as a real-time operational engine.

## Supported Interventions
- **Dispatch +1 Worker**: Models localized capacity addition to the active bottleneck.
- **Picking +5 Workers**: Models massive capacity addition to an upstream, unconstrained stage.
- **Packing +2 Workers**: Models moderate capacity addition to a downstream, unconstrained stage.
- **Productivity +10%**: Models a global reduction in raw processing times.
- **Extended Shift (10h to 12h)**: Models relaxing the daily operating boundary constraint.

## Key Visualizations & Analytics
- **KPI Comparisons**: Interactive metrics displaying Mean Flow Time, P95 Flow Time, Mean Waiting Time, and SLA Achievement. Absolute and relative percentage changes are color-coded intuitively.
- **Scenario Hypothesis Context**: A dynamic text field that clearly translates the selected mathematical scenario into a plain-English operational hypothesis and result.
- **Flow/Wait Visual Breakdown**: Side-by-side grouped bar charts for macroscopic comparison between Baseline and Simulation runs.
- **Stage-Level Queue Shift**: A grouped bar chart tracking precisely how queue lengths shift (or fail to shift) across specific operational stages due to the selected intervention.

## Interpretations
The dashboard makes it obvious that intervening on stages that are not active bottlenecks (like Picking or Packing) results in virtually zero system-level flow-time improvement, a foundational learning outcome for process modeling.
