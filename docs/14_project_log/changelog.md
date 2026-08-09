# Changelog

## [Unreleased]
- Initialized Module 1 Project Foundation.
- Initialized Module 2 Dataset Research and Specification. defined data dictionary, synthetic methodology, and data quality requirements.
- Initialized Module 3 Dataset Acquisition and Initial Data Inspection.
- Created public GitHub repository `ai-process-digital-twin` and configured Git workflow tracking `main` branch.
- Implemented Module 4.1 Data Loading & Immutable Raw Data Layer. Added pandas to dependencies and created rigorous loader tests.
- Implemented Module 4.2 Column Naming & Data Type Standardization. Standardized dtypes (string/float64/datetime64) across datasets and enforced snake_case.
- Implemented Module 4.3 Timestamp Validation. Developed a validation layer to evaluate missingness and temporal anomalies across the Olist lifecycle.
- Implemented Module 4.4 Missing-Value Analysis & Treatment. Classified missing records by intent and established explicit RETAIN_AS_NULL and EXCLUDE policies without fabricating operational realities.
- Implemented Module 4.5 Duplicate & Key Validation. Identified primary keys, composite keys, and structural repetition in the Olist dataset without destructive deduplication.
- Implemented Module 4.6 Referential Integrity Validation. Validated foreign-key relationships and documented the 100% core match rate and many-to-many review mappings.
- Implemented Module 4.7 Product Physical Data Validation. Validated physical product attributes (weight, dimensions) ensuring completeness and assessing distributions and outliers for digital-twin relevance.
- Implemented Module 4.8 Processed Dataset Construction. Built reproducible pipeline generating parquet-based processed datasets with explicit eligibility and physical validation flags, completing Module 4.
- Implemented Module 5.1 Operational Process Model & Synthetic Data Specification. Documented the 5-stage fulfillment process, schemas, calibration strategies, and validation rules without generating synthetic data yet.
- Implemented Module 5.2 Synthetic Operational Data Generation. Built deterministic pipeline simulating worker and shift-constrained execution of 99,281 orders, producing 496,405 warehouse stage records calibrated against carrier dispatch boundaries.
- Implemented Module 5.3 Synthetic Data Quality & Statistical Validation. Verified 100% structural and temporal integrity of the dataset. Documented expected extreme queues causing 3.20% carrier handover anomaly, mapping strong wait-queue correlations across simulated stages.
- Implemented Module 5.4 Operational Scenario & Sensitivity Configuration. Designed deterministic configuration framework and registered 6 OFAT (One-Factor-At-A-Time) experimental scenarios based on the validated baseline constraints.
- Implemented Module 5.5 Baseline Scenario Execution & KPI Extraction. Established core process performance metrics across flow time, SLA, stage utilization, and queuing behaviors for the canonical digital twin baseline.
- Implemented Module 5.6.1 Dispatch Capacity What-If Experiment. Evaluated adding +1 worker capacity to the Dispatch stage via deterministic simulation, comparing queue and flow-time performance against the operational baseline.
- Implemented Module 5.6.2 Picking Capacity What-If Experiment. Evaluated adding +5 worker capacity to the Picking stage to measure upstream relief on downstream queues.
- Implemented Module 5.6.3 Packing Capacity What-If Experiment. Evaluated adding +2 worker capacity to the Packing stage to measure downstream bottlenecks when adding capacity to a low-utilization stage.
