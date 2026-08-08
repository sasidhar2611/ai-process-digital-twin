# Assumptions

The following assumptions are formally defined for the synthetic data generation and digital twin simulation phases:

## Data Deletion & Filtering
- **Data Deletion Strategy**: The original raw data remains immutable. No rows are completely deleted from the database or the primary `data/processed/` analytical datasets.
- **Analytical Filtering Strategy**: Ineligible or incomplete rows are flagged (e.g., `eligible_for_demand_timeline`, `physical_data_complete`) and kept in the processed datasets. The downstream processes (such as the discrete-event simulation) must filter rows dynamically on-the-fly rather than consuming destructive datasets.

## Business Process
- [ASSUMPTION] Fulfillment operations follow a strictly linear sequence: Order Processing -> Picking -> Packing -> Sorting -> Dispatch.
- [REAL] `order_approved_at` represents the actual payment approval timestamp.
- [ASSUMPTION] Warehouse processing availability is anchored from this approval/release point for future modeling (it is NOT an actual measured warehouse-arrival timestamp).

## Workforce & Capacity
- [ASSUMPTION] Workers are assigned to specific stages and do not dynamically reallocate during a shift.
- [ASSUMPTION] Processing times follow a Lognormal distribution, subject to variation based on real product weight and dimensions.

## Operating Hours
- [ASSUMPTION] The synthetic fulfillment center operates on a standardized schedule (e.g., 2 shifts, 06:00 to 22:00, Monday to Saturday). Off-hour orders accumulate in queues.

## Missing Data
- [ASSUMPTION] Orders missing `order_approved_at` cannot be synthesized and are strictly EXCLUDED_FROM_ANALYSIS in the simulation layer.
- [ASSUMPTION] Products missing physical dimensions cannot undergo volumetric capacity simulation and must be flagged or excluded from capacity checks.
