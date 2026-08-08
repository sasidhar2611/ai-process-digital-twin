# Processed Datasets

## Overview
This document describes the PROCESSED DATASET layer constructed in Module 4.8. These datasets are analysis-ready, reproducible, and derived strictly from real Olist data without synthetic operational assumptions.

## Data Lineage
RAW (`data/raw/olist/`)
 ↓
LOADED (Immutable Read)
 ↓
STANDARDIZED (Data Types, Snake Case)
 ↓
VALIDATED (Module 4.1-4.7 Rules applied/verified)
 ↓
PROCESSED (`data/processed/*.parquet`)

## Processed Datasets

All processed datasets retain 100% of their source rows. No records are deleted. Instead, eligibility and completeness are managed via explicit analytical flags.

### 1. processed_orders
**Source Rows**: 99,441 | **Processed Rows**: 99,441
- **Derived Fields**:
  - `delivery_delay_days` (DERIVED DATA): `order_delivered_customer_date` - `order_estimated_delivery_date`.
- **Eligibility Flags** (ANALYSIS FLAG):
  - `has_approved_timestamp`: True if `order_approved_at` is not null.
  - `eligible_for_demand_timeline`: True if `has_approved_timestamp` is true.
  - `is_delivered_timestamp_complete`: True if both carrier and customer delivery dates are not null.
  - `eligible_for_delivery_kpi`: True if status is 'delivered' and `is_delivered_timestamp_complete` is true.

### 2. processed_products
**Source Rows**: 32,951 | **Processed Rows**: 32,951
- **Derived Fields**:
  - `physical_volume_cm3` (DERIVED DATA): Length × Height × Width.
- **Physical Flags** (ANALYSIS FLAG):
  - `physical_data_complete`: True if weight, length, height, width are all present.
  - `physical_measurement_valid`: True if complete AND all dimensions/weight > 0.

### 3. processed_customers
**Source Rows**: 99,441 | **Processed Rows**: 99,441
- Retains both `customer_id` (order-level token) and `customer_unique_id` (cross-purchase identity).

### 4. processed_order_items
**Source Rows**: 112,650 | **Processed Rows**: 112,650
- Standardized timestamps (`shipping_limit_date`) and numeric conversions.

### 5. processed_sellers
**Source Rows**: 3,095 | **Processed Rows**: 3,095
- Standardized strings and zip codes.

### 6. processed_payments
**Source Rows**: 103,886 | **Processed Rows**: 103,886
- Standardized payment types, sequential indices, and values.

### 7. processed_reviews
**Source Rows**: 99,224 | **Processed Rows**: 99,224
- Standardized timestamps. Note that `review_id` is retained as-is, representing a many-to-many relationship where applicable.

## Row Retention Policy
No rows were dropped during processed dataset construction. Downstream models will filter dynamically based on the explicit `eligible_*` and `valid_*` flags, preserving the immutable baseline.

## Determinism & Data Quality
The build pipeline (`src/data/processed_dataset_builder.py`) is fully deterministic and validated:
- Raw checksums unchanged.
- Keys uniqueness and referential integrity preserved.
- Output format: Parquet for optimal analytical performance.
