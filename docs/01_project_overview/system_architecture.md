# System Architecture

This document describes the actual implemented architecture of the AI-Process-Digital-Twin project as of Module 5.8.

## Architecture Diagram

REAL OLIST DATA
↓
RAW DATA LAYER
↓
DATA LOADING
↓
STANDARDIZATION
↓
DATA QUALITY VALIDATION
↓
PROCESSED DATA
↓
SYNTHETIC OPERATIONAL MODEL
↓
SYNTHETIC VALIDATION
↓
SCENARIO CONFIGURATION
↓
BASELINE EXECUTION
↓
WHAT-IF SCENARIOS
↓
KPI EXTRACTION
↓
BOTTLENECK ANALYSIS
↓
VISUALIZATION / DEPLOYMENT (Future)

## Layer Explanations

### 1. Real Olist Data
- **Purpose**: Ground the simulation in reality using actual e-commerce demand distributions.
- **Input**: Kaggle (or raw downloaded) Olist datasets.
- **Output**: Physical CSV files stored locally.
- **Important Files**: `olist_orders_dataset.csv`, `olist_order_items_dataset.csv`, `olist_products_dataset.csv`.
- **Relationship**: Feeds the Raw Data Layer.

### 2. Raw Data Layer
- **Purpose**: Physical storage layer preventing tracking of raw, uncompressed operational data in Git.
- **Input**: External datasets.
- **Output**: Ignored directory files.
- **Important Files**: `data/raw/*`, `.gitignore`.
- **Relationship**: The extraction point for Data Loading.

### 3. Data Loading
- **Purpose**: Read physical files into Pandas DataFrames safely with schema checks.
- **Input**: `data/raw/*.csv`
- **Output**: Pandas DataFrames.
- **Important Files**: `src/data/raw_data_loader.py`.
- **Relationship**: Feeds the Standardizer.

### 4. Standardization
- **Purpose**: Standardize real Olist datasets (handling missing data, inferring physical dimensions).
- **Input**: Raw DataFrames.
- **Output**: Standardized DataFrames.
- **Important Files**: `src/data/standardizer.py`, `src/data/missing_data_handler.py`.
- **Relationship**: Ensures clean data for Validation.

### 5. Data Quality Validation
- **Purpose**: Enforce strict data quality rules (referential integrity, physical limits).
- **Input**: Standardized DataFrames.
- **Output**: Validated DataFrames.
- **Important Files**: `src/validation/data_validator.py`, `src/validation/referential_integrity.py`.
- **Relationship**: Ensures no dirty data corrupts the simulation; passes data to Processed Data.

### 6. Processed Data
- **Purpose**: Persist clean, typed data into efficient columnar Parquet formats.
- **Input**: Validated DataFrames.
- **Output**: `.parquet` files in `data/processed/`.
- **Important Files**: `src/data/processed_data_builder.py`.
- **Relationship**: Becomes the immutable foundational dataset for the synthetic generator.

### 7. Synthetic Operational Model
- **Purpose**: Generate synthetic warehouse processing timestamps based on real Olist demand, applying a 5-stage fulfillment process (Processing, Picking, Packing, Sorting, Dispatch).
- **Input**: Processed Parquet DataFrames.
- **Output**: Synthetic Event DataFrame.
- **Important Files**: `src/synthetic/generator.py`, `src/synthetic/config.py`.
- **Relationship**: Generates the baseline simulated events.

### 8. Synthetic Validation
- **Purpose**: Validate that generated synthetic events conform to expected distributions, physical limits, and configured rules.
- **Input**: Synthetic Event DataFrame.
- **Output**: Validation report / exception raising.
- **Important Files**: `src/synthetic/validation.py`.
- **Relationship**: Ensures model output is logically sound before execution.

### 9. Scenario Configuration
- **Purpose**: Define structured operational parameters (shift hours, worker capacity, productivity).
- **Input**: JSON configuration files.
- **Output**: `ScenarioDefinition` objects.
- **Important Files**: `src/synthetic/scenario.py`, `config/scenarios/*.json`.
- **Relationship**: Controls the parameters for Baseline and What-If executions.

### 10. Baseline Execution
- **Purpose**: Generate the canonical "default" synthetic operational dataset under normal parameters.
- **Input**: Baseline Configuration, Processed Data.
- **Output**: Baseline Synthetic DataFrame.
- **Important Files**: `scripts/execute_baseline.py`, `config/scenarios/baseline.json`.
- **Relationship**: Establishes the control group for scenario comparisons.

### 11. What-If Scenarios
- **Purpose**: Modify isolated constraints (capacity, shifts, productivity) and regenerate the synthetic timeline to measure impact.
- **Input**: Scenario Configurations, Processed Data.
- **Output**: Modified Synthetic DataFrames.
- **Important Files**: `scripts/execute_*.py`.
- **Relationship**: Generates comparative data for analysis.

### 12. KPI Extraction
- **Purpose**: Extract consistent business metrics (flow time, waiting time, utilization, queue lengths).
- **Input**: Synthetic DataFrames.
- **Output**: JSON summaries and Parquet metric tables.
- **Important Files**: `src/synthetic/kpi.py`.
- **Relationship**: Quantifies scenario performance for the Bottleneck Analyzer.

### 13. Bottleneck Analysis
- **Purpose**: Formally identify constraints and rank interventions using deterministic scoring logic.
- **Input**: KPI JSONs and Stage Metrics.
- **Output**: Ranked intervention results and bottleneck candidates.
- **Important Files**: `src/analysis/bottleneck_analyzer.py`.
- **Relationship**: Final analytical layer that provides business insights.

### 14. Visualization / Deployment (Future)
- **Purpose**: Make the insights accessible via interactive dashboards or deployed systems.
- **Status**: Not yet implemented.
