# Data Standardization Strategy

## Overview
This document outlines the standardizations applied to the Olist datasets in memory to prepare them for the digital twin simulation and downstream analytics, without modifying the raw source CSVs.

## Naming Convention
- **Standard**: `snake_case` is enforced across all column names.
- **Rule**: No meaningful Olist fields are arbitrarily renamed. Semantic meaning is strictly preserved.
- **Exceptions**: Explicit typos are corrected (e.g., `product_name_lenght` -> `product_name_length`).

## Data Type Conventions
The `DataStandardizer` maps logical concepts to explicit Pandas datatypes:

### Timestamps
All dates and times are converted to `datetime64` using `pd.to_datetime(..., errors='coerce')`. 
- `order_purchase_timestamp`
- `order_approved_at`
- `order_delivered_carrier_date`
- `order_delivered_customer_date`
- `order_estimated_delivery_date`
- `shipping_limit_date`
- `review_creation_date`
- `review_answer_timestamp`

### Numeric Fields
Measurements, prices, and dimensional data are cast to `float64` (`pd.to_numeric(..., errors='coerce')`). We use float64 as the base representation to safely allow missing values (NaN) during standard loads.
- `price`, `freight_value`, `payment_value`
- `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`, `product_name_length`, `product_description_length`, `product_photos_qty`

### Categorical and Text Fields
Identifiers and textual categories are enforced as `string` using `.astype("string")`.
- `order_id`, `customer_id`, `product_id`, `seller_id`, `order_item_id`
- `order_status`, `customer_state`, `seller_state`, `product_category_name`

## Raw Data Immutability
All standardization happens dynamically in memory. The source files inside `data/raw/olist/` are NEVER altered. Row counts are strictly maintained (no dropping rows for NaNs at this stage).
