# Missing Value Analysis & Treatment

## Overview
This document outlines the systematic analysis of missing values in the Olist dataset and establishes the explicit treatment policies applied before downstream modeling.

## 1. Missingness Summary & Classifications

### 1.1 Orders Dataset
- **`order_approved_at`**: 160 missing (0.16%). 
  - *Classification*: `POTENTIAL_DATA_QUALITY_ISSUE` (160)
  - *Context*: Because this timestamp is intended to serve as the demand/release anchor for the digital twin, orders lacking this timestamp cannot enter the synthetic simulation properly.
- **`order_delivered_carrier_date`**: 1,783 missing (1.79%).
  - *Classification*: `EXPECTED_MISSING` (1,781) - Orders that were canceled, unavailable, or have not yet reached shipping.
  - *Classification*: `POTENTIAL_DATA_QUALITY_ISSUE` (2) - Orders that are marked as shipped/delivered but lack a carrier handover timestamp.
- **`order_delivered_customer_date`**: 2,965 missing (2.98%).
  - *Classification*: `EXPECTED_MISSING` (2,957) - Orders that were canceled, unavailable, or are still in transit.
  - *Classification*: `POTENTIAL_DATA_QUALITY_ISSUE` (8) - Orders explicitly marked as `delivered` but lacking the delivery timestamp.

### 1.2 Products Dataset
- **Physical Dimensions** (`product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`): 2 missing (0.01%).
  - *Classification*: `POTENTIAL_DATA_QUALITY_ISSUE` (2)
  - *Context*: Missing physical dimensions disrupt volumetric calculations required for synthetic picking/packing simulation.
- **Text/Category Metadata** (`product_category_name`, `product_name_length`, etc.): 610 missing (1.85%).
  - *Classification*: `EXPECTED_MISSING` (Optional metadata).

### 1.3 Order Reviews Dataset
- **`review_comment_title`**: 87,656 missing (88.3%).
- **`review_comment_message`**: 58,247 missing (58.7%).
  - *Classification*: `EXPECTED_MISSING` - Text reviews are entirely optional for customers.

### 1.4 Fully Complete Datasets
The following datasets contain zero missing values in required fields:
- `order_items`
- `customers`
- `sellers`
- `order_payments`

## 2. Treatment Policy

The overarching policy for this pipeline is strict adherence to **Raw Data Immutability** and avoidance of fabricated operational reality.

| Field | Treatment | Rationale |
|-------|-----------|-----------|
| `order_approved_at` | `RETAIN_AS_NULL` | We do NOT fabricate payment approval times. Future modeling steps must `EXCLUDE_FROM_ANALYSIS` (filter out) these 160 records when generating synthetic operations, as they lack a start anchor. |
| Delivery Timestamps | `RETAIN_AS_NULL` | We do NOT fabricate delivery operations. The 8 delivered orders missing timestamps will be excluded from transit-time KPIs. Expected missing dates remain NULL naturally. |
| Product Dimensions | `RETAIN_AS_NULL` | We do not replace with zero, as zero-volume physical goods violate simulation logic. Items mapping to these 2 products must be flagged or excluded in volumetric routing. |
| Review Text | `RETAIN_AS_NULL` | NLP or sentiment modules will simply ignore NULLs. |

### Imputation
- **Statistical Imputation:** `NONE`. There is no domain justification to guess when a specific customer paid or when a specific truck arrived.

### Exclusions
- Explicit exclusions (dropping rows) are **NOT** performed at the standardized data layer. The `MissingValueHandler` outputs DataFrames identical in row count to the raw input, ensuring all data remains queryable. Downstream modules (e.g., the synthetic data generator or KPI engine) will apply dynamic filters based on these known NULLs.
