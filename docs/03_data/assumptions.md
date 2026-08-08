# Assumptions

The following assumptions are formally defined for the synthetic data generation and digital twin simulation phases:

## Business Process
- [ASSUMPTION] Fulfillment operations follow a strictly linear sequence: Order Processing -> Picking -> Packing -> Sorting -> Dispatch.
- [ASSUMPTION] The real `order_approved_at` timestamp perfectly represents the moment an order drops into the warehouse system.

## Workforce & Capacity
- [ASSUMPTION] Workers are assigned to specific stages and do not dynamically reallocate during a shift.
- [ASSUMPTION] Processing times follow a Lognormal distribution, subject to variation based on real product weight and dimensions.

## Operating Hours
- [ASSUMPTION] The synthetic fulfillment center operates on a standardized schedule (e.g., 2 shifts, 06:00 to 22:00, Monday to Saturday). Off-hour orders accumulate in queues.
