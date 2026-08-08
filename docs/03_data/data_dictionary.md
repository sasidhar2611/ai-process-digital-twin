# Data Dictionary

## 1. Real Data Specification (From Olist Dataset)

| Category | Source Table | Original Column Name | Standardized Column Name | Data Type | Business Meaning | Required | Why Needed |
|----------|--------------|----------------------|--------------------------|-----------|------------------|----------|------------|
| Identity | olist_orders | order_id | order_id | String | Unique order identifier | Yes | Primary key connecting real demand to synthetic operations |
| Identity | olist_order_items | order_item_id | order_item_id | Integer | Sequence of item in order | Yes | Granular item tracking |
| Timing | olist_orders | order_purchase_timestamp | order_purchase_at | Datetime | When customer bought | Yes | Trigger for order arrival in simulation |
| Timing | olist_orders | order_approved_at | order_approved_at | Datetime | When payment approved | Yes | Represents start of fulfillment |
| Product | olist_products | product_id | product_id | String | Unique product identifier | Yes | Connects order to product traits |
| Product | olist_products | product_weight_g | product_weight_g | Float | Weight of product | Yes | Impacts packing/picking time |
| Product | olist_products | product_volume | (Calculated) | Float | Derived from dimensions | Yes | Determines bin size and capacity |
| Customer | olist_customers| customer_state | customer_state | String | Destination state | Yes | Impacts dispatch routing/sorting |

## 2. Synthetic Operational Data Specification

The following variables are REQUIRED for the digital twin but DO NOT exist in the public dataset. They will be synthesized later.

### Process Variables
- **stage**: String (e.g., 'Picking', 'Packing') - Identifies the fulfillment step.
- **stage_sequence**: Integer - Order of operations (1 to N).
- **start_time**: Datetime - When an order starts processing at a stage.
- **end_time**: Datetime - When an order finishes processing.
- **processing_time**: Float (seconds) - Duration of active work.
- **waiting_time**: Float (seconds) - Time spent in queue.

### Workforce Variables
- **worker_id**: String - Unique identifier for synthetic staff.
- **worker_count**: Integer - Total staff available per stage.
- **productivity_factor**: Float - Modifier for standard processing time per worker.

### Capacity Variables
- **stage_capacity**: Integer - Maximum concurrent orders a stage can handle.
- **queue_capacity**: Integer - Maximum items waiting before blocking upstream.

### Metrics
- **queue_length**: Integer - Items waiting at start time.
- **utilization**: Float - Percentage of capacity used.
- **sla_breach_flag**: Boolean - Whether internal SLA was missed.
