# Validation Rules for Synthetic Data Generation

Before any synthetic operational records are finalized, the generated dataset must pass the following structural and logical validation checks.

## 1. Sequence & Continuity
- **Stage Count**: Every evaluated `order_id` MUST have exactly 5 records corresponding to the 5 stages.
- **Stage Sequence**: Stages MUST follow the exact order: `PROCESSING` (1) -> `PICKING` (2) -> `PACKING` (3) -> `SORTING` (4) -> `DISPATCH` (5).
- **Chronology**: `start_time` <= `end_time` for all records.
- **Dependency**: The `start_time` of Stage N+1 MUST be >= the `end_time` of Stage N. Overlaps are strictly forbidden.

## 2. Temporal Constraints
- **Processing Time**: `processing_time` >= 0. Negative durations are impossible.
- **Waiting Time**: `waiting_time` >= 0. Negative wait times are impossible.
- **Completion Check**: `end_time` MUST exactly equal `start_time` + `processing_time`.
- **Start Check**: `start_time` MUST exactly equal `arrival_time_at_stage` + `waiting_time`.
- **Shift Compliance**: No `processing_time` can occur outside the defined warehouse operating hours (e.g., 08:00 - 18:00). All processing must be strictly contained within shift bounds.

## 3. Resource Validity
- **Worker Count**: `worker_count` >= 1. There cannot be 0 workers assigned to active processing.
- **Productivity**: `productivity_factor` > 0. A factor of 0 implies infinite processing time.
- **Queue**: `queue_length` >= 0.

## 4. Determinism
- Running the data generation pipeline twice with the same configuration and random seed MUST yield bit-for-bit identical parquet outputs.
