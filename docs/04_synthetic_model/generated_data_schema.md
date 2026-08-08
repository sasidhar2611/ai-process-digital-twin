# Generated Data Schema

The `synthetic_operational_data.parquet` file implements the following flattened schema. Note that fields marked as `SYNTHETIC` represent simulation outputs based on our assumptions and were never historically measured by Olist.

## Core Linkage
- `order_id` (string): REAL - Foreign key mapping back to `processed_orders`.

## Operational Variables
- `stage` (string): SYNTHETIC - Name of the operational stage (e.g. PROCESSING, PICKING).
- `stage_sequence` (int64): SYNTHETIC - Integer sequence of the stage (1 to 5).
- `start_time` (datetime64[ns]): SYNTHETIC - Assigned simulation start timestamp.
- `end_time` (datetime64[ns]): SYNTHETIC - Assigned simulation completion timestamp.
- `processing_time` (float64): SYNTHETIC - Active duration in seconds.
- `waiting_time` (float64): SYNTHETIC - Queue wait duration in seconds.

## Resource Assignments
- `worker_id` (int64): SYNTHETIC - Unique ID of the worker processing the stage.
- `worker_count` (int64): SYNTHETIC - Global capacity for the stage.
- `productivity_factor` (float64): SYNTHETIC - Normal-distributed multiplier for worker speed.
- `queue_length` (int64): SYNTHETIC - Count of items in queue at the time of arrival.

## Contextual Drivers
- `item_count` (int64): DERIVED - Number of physical items in the order.
- `total_weight_g` (float64): DERIVED - Sum of product weights.
- `total_volume_cm3` (float64): DERIVED - Sum of product volumes.
