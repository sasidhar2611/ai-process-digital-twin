# Decisions Log

## Module 1
- Initialized standard repository structure.
- Created virtual environment and Git repository.
- Decided on strict module-by-module architecture strategy.
- Created public GitHub repository and established local-to-remote tracking, ensuring raw datasets are excluded.

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
