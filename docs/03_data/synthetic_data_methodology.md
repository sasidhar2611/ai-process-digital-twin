# Synthetic Data Methodology

## Overview
Because the Olist dataset lacks internal warehouse timestamps and resource data, we will synthesize these operational mechanics using the real `order_id` and `order_approved_at` timestamps as anchors.

## Data Relationship Design
The primary linkage key between REAL ORDER DATA and SYNTHETIC PROCESS OPERATIONS will be `order_id`. 
Each real `order_id` will spawn a sequence of synthetic operational records in a new table (e.g., `synthetic_operations`), mapping 1-to-many.

## Generation Methodology

1. **Order Arrival Anchor**: The real `order_approved_at` will serve as the arrival event `t=0` in the fulfillment center.
2. **Productivity Modifiers**: Using real product dimensions (weight/volume) and order complexity (item count), we will calculate baseline operational effort.
3. **Stochastic Processing**: 
   - Processing time will be generated using probability distributions (e.g., Gamma or Lognormal) anchored to baseline effort.
   - Example [ASSUMPTION]: Picking time $\sim Lognormal(\mu, \sigma)$ based on item count.
4. **Shift Constraints**: Synthetic timestamps will only advance during defined working hours. Orders arriving off-hours will queue.
5. **Stage Progression**:
   - Picking -> Packing -> Sorting -> Dispatch.
   - An order's `start_time` at a stage is the `end_time` of the previous stage + `waiting_time`.

## Lineage
PUBLIC DATA -> RAW DATA -> STANDARDIZED ORDER DATA -> COMBINED WITH SYNTHETIC OPERATIONAL DATA -> DIGITAL TWIN
