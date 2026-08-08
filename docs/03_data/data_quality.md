# Data Quality Requirements

Before integrating data into the digital twin, the following quality checks [PLANNED] must pass:

## Real Data Integrity
1. **Missing Values**: Ensure critical fields (`order_id`, `order_approved_at`) have known distributions. *(Update: order_approved_at has 160 missing values (0.16%). Policy: RETAIN_AS_NULL and exclude these records from operational timeline synthesis in downstream modules. See missing_value_analysis.md).*
2. **Duplicate Orders**: Assert `order_id` uniqueness. *(Update: Verified 100% unique in orders dataset during Module 4.5).*
3. **Timestamp Ordering**: Assert `order_purchase_timestamp` <= `order_approved_at` <= delivery timestamps. *(Update: Validation executed in Module 4.3. Found 1.39% violation for approved <= carrier. See timestamp_validation.md).*
4. **Orphan Relationships**: Ensure all items in `olist_order_items` match a valid `order_id` in `olist_orders`. *(Update: Verified 100% referential integrity across all core operational tables during Module 4.6. No true orphans exist. See referential_integrity.md).*
5. **Physical Plausibility**: Assert physical measurements (weight, dimensions) are positive non-zero values. *(Update: Verified 99.99% completeness during Module 4.7. Found 4 products with strictly zero weight (0g) which require domain validation. No negative values exist. See product_physical_validation.md).*
6. **Processed Layer Consistency**: Ensure processed analytical datasets maintain 100% row retention of source data, managing exclusions exclusively via analytical flags. *(Update: Verified 100% retention during Module 4.8. See processed_dataset.md).*

## Synthetic Data Integrity
1. **Logical Timestamps**: Ensure synthetic `end_time` >= `start_time` for all operations.
2. **Stage Sequence Validation**: Ensure Picking ends before Packing starts.
3. **Shift Alignment**: Ensure no active processing occurs outside defined working hours.
4. **Duplicate Operational Records**: Ensure combination of `order_id` + `stage` is unique.
