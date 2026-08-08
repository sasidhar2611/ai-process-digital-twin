# Operational Assumptions

This document lists the core FUTURE MODELING ASSUMPTIONS dictating the behavior of the synthetic warehouse model.

## 1. Processing Time Model
We assume base processing times are sampled from a Lognormal distribution (to prevent negative processing times and capture right-skewed operational delays). Base times are modified by specific real-data drivers:
- **PROCESSING**: Driven by generic order complexity (no direct scaling).
- **PICKING**: Driven by physical complexity (total volume `total_volume_cm3` and `item_count`). Heavier or multi-item orders require more time.
- **PACKING**: Driven by `item_count` and `total_weight_g`.
- **SORTING**: Driven by `customer_state` (destination complexity).
- **DISPATCH**: Driven by `total_weight_g`.

## 2. Worker Model
- **Assignment**: Workers are assigned to specific stages without dynamic reallocation.
- **Simultaneity**: A worker can only process one order's stage at a time.
- **Productivity**: Each worker has a fixed generic `productivity_factor` (multiplier applied to base processing time). Mean productivity = 1.0.

## 3. Shift Model
- **Operating Hours**: The warehouse is assumed to operate on a standardized daily shift schedule (e.g., 08:00 to 18:00).
- **Outside Hours**: Orders arriving or pending outside of shift hours will remain in the queue (accruing `waiting_time`) until the next shift begins.
- *(Note: Exact shift hours are currently configured as an assumption and require explicit approval/calibration during Module 5.2 execution).*

## 4. Queue Model
- **Policy**: FIFO (First-In-First-Out).
- **Mechanics**: Each stage has an infinite capacity queue. Orders enter the queue immediately upon completion of the previous stage. The `queue_length` is evaluated exactly when processing begins for that order.
- `waiting_time` = `start_time` - arrival_time_at_stage.

## 5. Multi-item Orders
- Real `order_items` data is aggregated per `order_id` to compute `item_count`, `total_weight_g`, and `total_volume_cm3`.
- The simulation processes orders as monolithic units (not individual items). Processing effort scales continuously based on these real aggregate drivers.
