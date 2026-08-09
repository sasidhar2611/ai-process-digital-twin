# Decisions Log

## Module 1
- Initialized standard repository structure.
- Created virtual environment and Git repository.
## Module 5.6.5
- Executed the `extended_shift` scenario evaluating the impact of extending the daily operating window from 10 hours to 12 hours.
- Used the `productivity_factor` correction fix implemented in Module 5.6.4 for accurate neutral execution.

## Module 5.6.4
- Fixed productivity utilization mechanism in `generator.py` to ensure `productivity_factor` from config is correctly used as the mean for processing times.
- Executed the `productivity_plus_10` scenario evaluating the impact of increasing productivity by 10%.
- Documented how global productivity improvements scale across stages.

## Module 5.6.3
- Executed the `packing_plus_2` scenario evaluating the impact of increasing Packing capacity from 10 to 12 workers.
- Evaluated whether increasing capacity in a stage with very low utilization produces any tangible system-level flow-time improvements.

## Module 5.6.2
- Executed the `picking_plus_5` scenario evaluating the impact of increasing Picking capacity from 15 to 20 workers.
- Addressed whether massive upstream capacity increases effectively relieve downstream bottlenecks or simply shift congestion further down the process pipeline.

## Module 5.6.1
- Executed the `dispatch_plus_1` scenario evaluating the impact of increasing Dispatch capacity from 3 to 4 workers.
- Concluded the model hypothesis was strongly supported: adding one dispatch worker significantly reduced dispatch queues and subsequently improved overall flow times.
- Decided to maintain baseline results as strictly read-only and generate independent scenario-specific output structures for safe comparison.

## Module 5.5
- Formalized KPI definitions including a configurable SLA assumption (5 Days) to measure operational adherence.
- Evaluated bottleneck metrics theoretically across the baseline simulation, identifying DISPATCH as the highest utilized stage (31.15%) though heavily constrained overall by shift-wait dynamics.

## Module 5.4
- Designed deterministic scenario configuration framework, strictly separating definition from execution.
- Adopted One-Factor-At-A-Time (OFAT) experimental methodology supported by a Common Random Seed Strategy.
- Serialized 6 initial experimental definitions to JSON (baseline, dispatch_plus_1, picking_plus_5, packing_plus_2, productivity_plus_10, extended_shift).

## Module 5.3
- Evaluated queue congestions driving the 3.20% carrier completion anomaly. Decided to classify these as EXPECTED_MODEL_VARIATION rather than artificially tuning the model, preserving realistic capacity constraints.
- Validated processing time correlation with physical complexities (e.g. Volume to Picking = 0.58).

## Module 5.2
- Generated synthetic warehouse operational dataset strictly tracing real `order_id`s, without fabricating missing physical attributes.
- Adopted sequential event-based loop to schedule workers and track queue lengths dynamically at arrival time, respecting a strict 08:00 - 18:00 operating shift.
- Validated external carrier completion plausibility, achieving ~97% logic consistency without artificially overriding generation equations.

## Module 5.1
- Formally defined 5 linear warehouse stages (PROCESSING, PICKING, PACKING, SORTING, DISPATCH) based strictly on Olist real order records.
- Explicitly isolated physical derived fields (e.g. `total_volume_cm3`) from pure synthetic fields (e.g. `processing_time`, `queue_length`) establishing strict REAL vs ASSUMPTION lineage.
- Documented Lognormal distribution baseline for processing times, FIFO queuing policy, and standardized shift operations for simulation configuration.

## Module 4.8
- Decided to build a single comprehensive processed dataset layer, saved in parquet format.
- Decided to implement row retention by preserving 100% of source records and maintaining explicit eligibility flags (e.g., `eligible_for_demand_timeline`) to prevent destructive data loss during downstream simulations.

## Module 4.7
- Validated physical attributes (weight, dimensions). Decided to treat statistical outliers as valid physical possibilities (e.g. large items).
- Decided to classify 4 items with exactly `0g` weight as requiring domain validation rather than arbitrarily correcting them. No negative dimensions found.
- Kept derived volume as purely analytical context rather than polluting the raw dataset.

## Module 4.6
- Verified 100% referential integrity across all core operational tables. No true orphans exist.
- Confirmed the translation dataset is a helper mapping, not a parent. Unmatched product categories are treated as `UNTRANSLATED_CATEGORY` rather than orphans.
- Documented a many-to-many relationship between reviews and orders.

## Module 4.5
- Validated dataset identities without mutation. Verified `customer_id` is a 1:1 order token, while `customer_unique_id` tracks the human.
- Identified `review_id` contains unexpected duplicates and should not be used as a strict primary key.
- Kept `geolocation` full-row duplicates (26%) as they represent valid recurring zip code bounding box coordinates rather than errors.

## Module 4.4
- Formalized missing value treatment strategy. Decided to RETAIN_AS_NULL for all missing fields globally to preserve absolute operational integrity and avoid fabricating synthetic reality.
- Analyzed missing delivery timestamps: 8 are anomalous, remaining are expected due to order status.
- Defined explicit EXCLUDE_FROM_ANALYSIS rule for orders lacking `order_approved_at` during the synthetic generation phase.

## Module 4.3
- Decided to create a standalone `TimestampValidator` class that strictly analyzes temporal sequences without mutating or repairing data, to explicitly separate validation from ETL.
- Distinguished between "Expected Missingness" (due to order status) and true anomalies.
- Formalized the business assumption that `order_approved_at` acts as a demand release anchor, clarifying that it is NOT a physical warehouse-arrival timestamp.

## Module 4.2
- Standardized all categorical/identifier fields to `string` dtype to prevent numeric operations on keys (like `customer_id` or `zip_code`).
- Standardized all continuous/numeric metrics to `float64` strictly. This allows Pandas to natively handle missing values (NaN) during standard loads without crashing or requiring row drops.
- Timestamps explicitly cast to `datetime64` using `coerce` so that malformed dates become `NaT` without dropping the row.
- Addressed dataset-specific typos (`lenght` to `length`) in product descriptions to preserve readability while maintaining semantic meaning.

## Module 4.1
- Decided to create a strict immutable Python data loading layer for raw datasets.
- Decided to add pandas to the requirements to handle CSV loading securely.
- Tests actively enforce file immutability using MD5 hashes and file stat modification checks.

## Module 2
- Selected Olist Brazilian E-Commerce dataset as the primary data source.
- Decided to synthesize internal warehouse timestamps and resource data using `order_id` as the primary linkage key.
- Established Lognormal stochastic processing based on real product dimensions for synthetic operations.
