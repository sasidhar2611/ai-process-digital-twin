# Synthetic Data Specification

This document defines the schema and categorization for the synthetic operational dataset that will be generated in Module 5.2.

## Real vs. Synthetic Categorization

### 1. REAL INPUTS
Fields directly measured and validated from the original Olist database.
- `order_id` (Primary Linkage)
- `order_purchase_timestamp`
- `order_approved_at` (Demand anchor)
- `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`
- Order status and delivery outcomes

### 2. DERIVED INPUTS
Metrics deterministically calculated from real inputs, not part of the synthetic operational layer itself.
- `physical_volume_cm3`
- `delivery_delay_days`
- `item_count` (Number of items per order)
- `total_weight_g`, `total_volume_cm3`

### 3. SYNTHETIC VARIABLES
Variables generated exclusively by the simulation model to represent warehouse operational states that were never measured by Olist.
- `stage` (String)
- `stage_sequence` (Integer)
- `start_time` (Datetime)
- `end_time` (Datetime)
- `processing_time` (Float)
- `waiting_time` (Float)
- `worker_id` (Integer)
- `worker_count` (Integer)
- `productivity_factor` (Float)
- `queue_length` (Integer)

## Schema Design

The final synthetic parquet dataset will flatten these variables per `order_id` and `stage`. One `order_id` will yield multiple rows (one for each process stage).

Example Schema per row:
- `order_id`: string
- `stage`: string
- `stage_sequence`: int64
- `start_time`: datetime64[us]
- `end_time`: datetime64[us]
- `processing_time`: float64
- `waiting_time`: float64
- `worker_id`: int64
- `worker_count`: int64
- `productivity_factor`: float64
- `queue_length`: int64

**Important Note**: Processing times, waiting times, and queue lengths are FUTURE MODELING ASSUMPTIONS and must never be interpreted as actual historical records from the Olist warehouse.
