# Operational Flow & Process Analysis Dashboard

## Purpose
The Operational Flow dashboard (Module 6.5) decomposes end-to-end fulfillment flow time into constituent processing and waiting components. Its primary objective is to visually distinguish true value-added processing time from systemic queuing delays.

## Data Source & Integrity
The dashboard reads exclusively from pre-aggregated analytical metrics:
- `dashboard_kpis.csv`: Contains top-level flow time, wait time, and processing time.
- `dashboard_stage_metrics.csv`: Contains stage-specific queueing, processing, and utilization data.

It does not recalculate, modify, or regenerate the underlying synthetic order events, preserving absolute deterministic integrity with the established baseline.

## Key Visualizations & Features
- **Sequential Process Flow**: Clearly highlights the `PROCESSING -> PICKING -> PACKING -> SORTING -> DISPATCH` operational sequence.
- **Total Flow Breakdown**: A pie chart emphasizing how waiting time dominates total flow time.
- **Stage Processing Time**: Bar chart showing the mean processing time configured and observed for each operational step.
- **Stage Waiting Time**: Bar chart highlighting where order accumulation causes delays. 
- **Queue and Utilization**: Comparative bar charts for queue depths and worker utilization to correlate constraints.

## Critical Interpretations
A core insight explicitly highlighted by the dashboard is the distinction between **Shift-Boundary Wait** and **Active Process Bottlenecks**:
- The `PROCESSING` stage accumulates the most waiting time not because of severe under-capacity, but due to overnight shift rollovers (incoming orders arrive 24/7, but operations only run 10 hours a day).
- Conversely, `DISPATCH` sustains the highest utilization and continuous intra-shift queueing, confirming it as the true active capacity constraint (Module 5.7 Bottleneck Analysis), despite having a lower raw total waiting time than `PROCESSING`.
