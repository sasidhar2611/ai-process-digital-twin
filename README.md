# AI Process Digital Twin

## 1. Overview
The AI-Process-Digital-Twin project is a robust synthetic operational simulator built on top of real-world e-commerce demand data from Olist. It allows organizations to safely execute and evaluate fulfillment center "what-if" scenarios (like adding workers, boosting productivity, or extending shifts) without risking live warehouse operations or requiring invasive telemetry integration.

## 2. Problem Statement
Real e-commerce transaction datasets (like Olist) typically lack granular warehouse operational telemetry (stage-level timestamps, queue lengths, worker utilization). This makes traditional operations research and bottleneck analysis impossible. This project solves this by generating highly controlled synthetic operational models anchored to real demand distributions.

## 3. Key Features
- **Data Engineering**: Cleanses and standardizes real Olist data with strict referential integrity.
- **Synthetic Digital Twin**: 5-stage sequential simulation (Processing, Picking, Packing, Sorting, Dispatch) driven by log-normal stochastic processing times, strict shift boundaries, and FIFO queueing.
- **Scenario Framework**: Declarative JSON-based "what-if" engine.
- **KPI Engine**: Automatically extracts Flow Time, Wait Time, Queues, and Utilization.
- **Bottleneck Analysis**: Multi-dimensional, normalized constraint identification to rank interventions.

## 4. Architecture Overview
The system architecture flows from physical real-world CSVs into a cleaned processed Parquet data layer. From there, the Synthetic Generator fabricates an operational reality (the Digital Twin) which is analyzed by the KPI Extractor and Bottleneck Analyzer.
*For more details, see [System Architecture](docs/01_project_overview/system_architecture.md) and [Data Lineage](docs/01_project_overview/data_lineage.md).*

## 5. Real vs Synthetic Data
- **Real Data**: Order approval times, item volumes, weights, counts.
- **Synthetic Data**: Stage processing durations, queue times, and internal timestamps. 

## 6. Result Summary (Synthetic Baseline vs What-Ifs)
**Baseline State**:
- Baseline Mean Flow Time: 21,901.68s
- Baseline Mean Waiting Time: 21,103.65s
- Baseline Bottleneck: **Dispatch** (Utilization: 31.15%, Mean Queue: 42.34)

**Intervention Results (Simulated)**:
- **Extended Shift (10h to 12h)**: -27.68% Flow Time Improvement (Addresses macro-boundary wait).
- **Dispatch Capacity +1**: -11.34% Flow Time Improvement (Most effective worker-capacity addition).
- **Productivity +10%**: -5.97% Flow Time Improvement.
- **Picking Capacity +5**: ~0.00% Flow Time Improvement (Stranded capacity / shifted bottleneck).
- **Packing Capacity +2**: ~0.00% Flow Time Improvement (Zero systemic benefit).

## 7. Testing
The system contains a rigorous test suite validating synthetic output logic, stochastic boundaries, scenario isolation, and analytical determinism.
`pytest tests/unit`

## 8. Repository Structure
- `config/`: Configuration for baseline and what-if scenarios.
- `data/`: Real, Derived, and Analytical data results (Raw/Parquet data is `.gitignored`).
- `docs/`: Formal logs, reports, methodology, and architecture definitions.
- `scripts/`: Python execution scripts for the various simulation stages.
- `src/`: Core classes for loading, validating, standardizing, synthetic generation, KPI extraction, and analysis.
- `tests/`: Extensive unit tests.

## 9. How to Run
1. Install dependencies: `pip install pandas pyarrow pytest scipy`
2. Ensure Olist raw datasets are placed in `data/raw/`
3. Execute Data pipeline: `python scripts/run_data_pipeline.py`
4. Execute Scenarios: `python scripts/execute_baseline.py`, followed by scenario scripts.
5. Execute Analysis: `python scripts/run_bottleneck_analysis.py`

## 10. Dashboard & Deployment
The dashboard synthesizes all simulated outputs into an interactive decision-support interface.

### Running Locally
To launch the dashboard locally:
```bash
streamlit run app/streamlit_app.py
```

### Streamlit Community Cloud
This project is deployment-ready for Streamlit Community Cloud. Simply deploy the repository and set the main file path to `app/streamlit_app.py`. No Docker or database is required, as the dashboard uses Git-tracked pre-computed data.

### Dashboard Access
Once running, the interactive multi-page dashboard will be accessible at: `http://localhost:8501`

## 10. Current Limitations
- Labor cost, energy usage, and real-world fatigue degradation are not modeled.
- Stage-to-stage travel times are assumed instant or integrated into base processing.

## 11. Planned Future Phases
- **Visualization & Deployment**: Dashboard-ready analytical datasets are prepared for the upcoming visualization and deployment phase. Transforming the analytical CSV files into an interactive BI Dashboard (e.g. Streamlit, PowerBI). Currently, no live dashboard or deployment exists.
