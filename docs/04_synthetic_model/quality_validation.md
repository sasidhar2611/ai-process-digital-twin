# Synthetic Data Quality Validation

This document verifies the structural and logical integrity of the synthetic operational dataset generated in Module 5.2.

## Quality Scorecard

| Check | Result | Status | Notes |
|-------|--------|--------|-------|
| **Order Linkage** | TRUE | PASS | All 99,281 generated synthetic order IDs map directly to the `processed_orders` layer. No fabricated IDs. |
| **Stage Completeness** | TRUE | PASS | Every eligible order has exactly 5 stage records. |
| **Stage Continuity** | TRUE | PASS | Stages are exactly 1-5 without omissions. |
| **Timestamp Validity** | TRUE | PASS | `end_time` == `start_time` + `processing_time`. `start_time` >= `order_approved_at`. |
| **Shift Compliance** | TRUE | PASS | All active processing starts strictly within the 08:00–18:00 warehouse operating window. Off-hours waiting is tracked in `waiting_time`. |
| **Worker Validity** | TRUE | PASS | `worker_count` >= 1. Workers belong to correctly configured stage pools. |
| **Queue Validity** | TRUE | PASS | `queue_length` >= 0 for all arrivals. Follows strict chronological tracking. |
| **Processing Time Validity** | TRUE | PASS | `processing_time` >= 0 for all records. |
| **Waiting Time Validity** | TRUE | PASS | `waiting_time` >= 0 for all records. |

## Determinism & Provenance
Regenerating the data with Random Seed 42 against the exact configuration parameters yields 100% bit-for-bit equivalence in the simulated temporal sequences. 

## Extreme Value Assessment
- **Processing Time**: Max recorded is ~4,920s (~1.3 hours) in PICKING. Expected model variation based on highly skewed product volume inputs.
- **Waiting Time**: Max recorded is ~155,020s (~43 hours) in DISPATCH. This spans over a weekend or multiple off-shift periods, fully expected in an 08:00-18:00 bounded operation.
- **Queue Length**: Max recorded is 867 items in PROCESSING. This occurs during peak simulated arrival bursts and is an expected queue buildup under the modeled constant capacity assumption.
- **Verdict**: EXPECTED_MODEL_VARIATION. No physical or mathematical defect detected in generation scaling.
