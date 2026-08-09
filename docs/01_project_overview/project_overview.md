# Project Overview

## 1. Project Objective
To construct a robust Synthetic Digital Twin of an e-commerce fulfillment operation (using real Olist demand data) that empowers formal bottleneck analysis and operational "what-if" scenario testing.

## 2. Problem Statement
Real e-commerce transaction datasets (like Olist) typically lack granular warehouse operational telemetry (stage-level timestamps, queue lengths, worker utilization). This makes traditional operations research and bottleneck analysis impossible without generating highly controlled synthetic operational models anchored to that real demand data.

## 3. Motivation
Warehouse operational efficiency directly dictates flow time and SLA achievement. By creating a digital twin that synthetically mimics operations on top of real-world order volumes, organizations can safely evaluate capital or labor investments (like adding workers or extending shifts) without risking live fulfillment processes.

## 4. Scope
- Data ingestion, cleaning, and validation of real Olist datasets.
- Development of a 5-stage synthetic digital twin simulation.
- Execution of baseline and what-if operational scenarios.
- Extraction of complex KPIs (queue lengths, utilizations, flow times).
- Formal bottleneck identification and intervention ranking.
- **Out of Scope**: Real-world operational execution, external logistics carrier simulation, live dynamic data ingestion.

## 5. Implemented Functionality
- **Data Engineering**: Schema validation, physical imputation, and Parquet serialization.
- **Synthetic Digital Twin**: Log-normal stochastic processing times bounded by strict 10-hour/12-hour shift logic and FIFO queues.
- **Scenario Framework**: Deterministic "what-if" experiment execution.
- **KPI Engine**: Calculation of Mean Flow Time, Mean Waiting Time, P95 metrics, Stage Utilization, and Queues.
- **Analytical Engine**: Multi-dimensional normalized bottleneck scoring and systemic intervention ranking.

## 6. Real vs Synthetic Data Distinction
- **Real Data**: The orders, items, products, approval dates, volumes, weights, and overarching demand distributions from the real Olist e-commerce dataset.
- **Synthetic Data**: The internal warehouse timestamps (processing start, processing end, wait times) at each simulated stage (Processing, Picking, Packing, Sorting, Dispatch).

## 7. Major Assumptions
- Order arrivals that fall outside of operating shift hours queue until the shift begins.
- Processing times follow a log-normal distribution scaled by a defined base rate and driven by variables like item count or volume.
- Workers do not experience fatigue or variable productivity beyond the stochastic variance in the model.
- Stages process sequentially without network cycle routing or defects.

## 8. Limitations
- The system models a synthetic operational reality, not the actual Olist warehouse.
- Cost constraints (labor wages, overtime, energy) are completely ignored.
- The simulation operates offline rather than interacting dynamically as an environment for real-time AI agents.

## 9. Current Project Status
- Complete through Module 5.7. The core data engineering, digital twin simulation, scenario execution, and formal bottleneck analysis are complete, tested, and validated.

## 10. Future Phase
- **Visualization & Deployment**: Transforming the resulting Parquet metrics and JSON summaries into an accessible format (e.g., Dashboards, interactive BI tools).
