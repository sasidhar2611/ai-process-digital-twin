# Data Quality Requirements

Before integrating data into the digital twin, the following quality checks [PLANNED] must pass:

## Real Data Integrity
1. **Missing Values**: Ensure critical fields (`order_id`, `order_approved_at`) have zero nulls.
2. **Duplicate Orders**: Assert `order_id` uniqueness.
3. **Timestamp Ordering**: Assert `order_purchase_timestamp` <= `order_approved_at` <= delivery timestamps.
4. **Orphan Relationships**: Ensure all items in `olist_order_items` match a valid `order_id` in `olist_orders`.

## Synthetic Data Integrity
1. **Logical Timestamps**: Ensure synthetic `end_time` >= `start_time` for all operations.
2. **Stage Sequence Validation**: Ensure Picking ends before Packing starts.
3. **Shift Alignment**: Ensure no active processing occurs outside defined working hours.
4. **Duplicate Operational Records**: Ensure combination of `order_id` + `stage` is unique.
