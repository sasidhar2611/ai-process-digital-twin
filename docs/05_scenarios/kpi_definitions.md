# KPI Definitions

This document strictly defines the Key Performance Indicators (KPIs) calculated during scenario executions to ensure identical analytical methodologies across scenarios.

## 1. Flow Time
**Definition**: The total elapsed time from when an order's demand is released to the warehouse until its final dispatch.
**Formula**: `dispatch_end_time - demand_release_time`
**Context**: 
- `demand_release_time` = `order_approved_at`.
- `dispatch_end_time` = The `end_time` of the DISPATCH stage (Stage 5).
**Unit**: Seconds.

## 2. Total Processing Time
**Definition**: The sum of active touch-time processing across all five fulfillment stages.
**Formula**: `sum(processing_time)`
**Unit**: Seconds.

## 3. Total Waiting Time
**Definition**: The sum of non-value-added waiting time in queues across all stages, including off-shift pauses.
**Formula**: `sum(waiting_time)`
**Unit**: Seconds.

## 4. SLA (Service Level Agreement)
**Definition**: The maximum permitted Flow Time before an order is considered delayed.
**Assumption**: 5 Days (432,000 seconds). This is a purely synthetic modeling assumption to provide a threshold for SLA adherence tracking. It is NOT a real-world measured SLA from Olist.
**Metrics**:
- `sla_met`: `flow_time <= 432000.0`
- `sla_achievement_percentage`: `mean(sla_met) * 100`

## 5. Queue Length
**Definition**: The number of orders physically waiting at a specific stage exactly when a new order arrives to join that queue.
**Reporting**: Evaluated individually per stage (mean, median, P95, maximum) rather than aggregating a meaningless total average across the warehouse.

## 6. Stage & Worker Utilization
**Definition**: The ratio of active processing work compared to the theoretical maximum available labor time over the simulation duration.
**Formula**: `stage_utilization = total_processing_time_sum / (worker_count * shift_duration_seconds * active_days)`
**Context**:
- `shift_duration_seconds`: Fixed to 10 hours (36,000s) based on the 08:00–18:00 schedule.
- `active_days`: The unique calendar days where the stage actively began processing tasks.
- In this model, since dynamic reassignment is disabled, `worker_utilization` is structurally identical to `stage_utilization`.
