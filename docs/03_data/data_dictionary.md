# Data Dictionary

## 1. Real Data Specification (From Olist Dataset)

| Dataset | Original Column Name | Standardized Column Name | Data Type | Meaning | Transformation Performed | Reason for Transformation |
|---------|----------------------|--------------------------|-----------|---------|--------------------------|---------------------------|
| `orders` | `order_id` | `order_id` | `string` | Unique order identifier | UNCHANGED | Already complies with standard |
| `orders` | `customer_id` | `customer_id` | `string` | Unique customer relation | UNCHANGED | Already complies with standard |
| `orders` | `order_purchase_timestamp` | `order_purchase_timestamp` | `datetime64` | When customer bought | STANDARDIZED (Type cast) | Required for temporal analysis |
| `orders` | `order_approved_at` | `order_approved_at` | `datetime64` | When payment approved | STANDARDIZED (Type cast) | Required for temporal analysis |
| `orders` | `order_delivered_carrier_date` | `order_delivered_carrier_date` | `datetime64` | When given to carrier | STANDARDIZED (Type cast) | Required for temporal analysis |
| `orders` | `order_delivered_customer_date` | `order_delivered_customer_date` | `datetime64` | When received by customer | STANDARDIZED (Type cast) | Required for temporal analysis |
| `orders` | `order_estimated_delivery_date` | `order_estimated_delivery_date` | `datetime64` | Estimated delivery | STANDARDIZED (Type cast) | Required for temporal analysis |
| `orders` | `order_status` | `order_status` | `string` | Status of the order | UNCHANGED | Already complies with standard |
| `order_items` | `order_id` | `order_id` | `string` | Order foreign key | UNCHANGED | Already complies with standard |
| `order_items` | `order_item_id` | `order_item_id` | `string` | Sequence of item in order | UNCHANGED | Already complies with standard |
| `order_items` | `product_id` | `product_id` | `string` | Product foreign key | UNCHANGED | Already complies with standard |
| `order_items` | `seller_id` | `seller_id` | `string` | Seller foreign key | UNCHANGED | Already complies with standard |
| `order_items` | `shipping_limit_date` | `shipping_limit_date` | `datetime64` | Limit for seller dispatch | STANDARDIZED (Type cast) | Required for temporal analysis |
| `order_items` | `price` | `price` | `float64` | Item price | STANDARDIZED (Type cast) | Enforce numeric format |
| `order_items` | `freight_value` | `freight_value` | `float64` | Item freight cost | STANDARDIZED (Type cast) | Enforce numeric format |
| `products` | `product_id` | `product_id` | `string` | Unique product identifier | UNCHANGED | Already complies with standard |
| `products` | `product_category_name` | `product_category_name` | `string` | Category of product | UNCHANGED | Already complies with standard |
| `products` | `product_name_lenght` | `product_name_length` | `float64` | Length of product name | STANDARDIZED (Rename, Type cast) | Fix typo, enforce numeric |
| `products` | `product_description_lenght`| `product_description_length` | `float64` | Length of description | STANDARDIZED (Rename, Type cast) | Fix typo, enforce numeric |
| `products` | `product_photos_qty` | `product_photos_qty` | `float64` | Number of photos | STANDARDIZED (Type cast) | Enforce numeric format |
| `products` | `product_weight_g` | `product_weight_g` | `float64` | Weight of product | STANDARDIZED (Type cast) | Enforce numeric format |
| `products` | `product_length_cm` | `product_length_cm` | `float64` | Length of product | STANDARDIZED (Type cast) | Enforce numeric format |
| `products` | `product_height_cm` | `product_height_cm` | `float64` | Height of product | STANDARDIZED (Type cast) | Enforce numeric format |
| `products` | `product_width_cm` | `product_width_cm` | `float64` | Width of product | STANDARDIZED (Type cast) | Enforce numeric format |
| `customers` | `customer_id` | `customer_id` | `string` | Unique customer relation | UNCHANGED | Already complies with standard |
| `customers` | `customer_unique_id` | `customer_unique_id` | `string` | Customer absolute ID | UNCHANGED | Already complies with standard |
| `customers` | `customer_zip_code_prefix`| `customer_zip_code_prefix`| `float64` | Zip code prefix | STANDARDIZED (Type cast) | Enforce numeric format |
| `customers` | `customer_city` | `customer_city` | `string` | City of customer | UNCHANGED | Already complies with standard |
| `customers` | `customer_state` | `customer_state` | `string` | State of customer | UNCHANGED | Already complies with standard |

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

## 3. Missing Value Policy
- **IMPUTED**: None. We do not use statistical imputation for missing operational dates or physical dimensions (e.g., zero weights are treated as requiring domain validation, not imputed).
- **RETAIN_AS_NULL**: Applied to all missing fields globally (e.g., `order_approved_at`, `product_weight_g`, delivery dates, reviews).
- **EXCLUDE_FROM_ANALYSIS**: Downstream modeling dynamically filters out records that lack mandatory anchors (like `order_approved_at`) without removing them from the standardized baseline dataset.

## 4. Key Identifiers & Relationships
- **Orders**: `order_id` is the primary key. `customer_id` is unique per order (1:1), representing the order token, NOT the customer profile. All orders have 100% referential integrity with customers.
- **Customers**: `customer_unique_id` is the actual human buyer identifier (1:M with orders).
- **Order Items**: Composite key `order_id` + `order_item_id` is unique. 100% referential integrity with orders, products, and sellers.
- **Payments**: Composite key `order_id` + `payment_sequential` is unique. 100% referential integrity with orders.
- **Reviews**: `review_id` is NOT perfectly unique (814 duplicates exist). Do not use as a strict primary key. The relationship with orders is many-to-many (one review can cover multiple orders).
