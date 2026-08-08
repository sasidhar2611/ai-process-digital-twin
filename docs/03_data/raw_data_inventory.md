# Raw Data Inventory

## Dataset Acquisition Summary
- **Source**: Olist Brazilian E-Commerce Public Dataset (via Kaggle)
- **Location**: `data/raw/olist/`
- **Acquisition Date**: August 8, 2026
- **Status**: Raw CSV files successfully acquired and placed in the designated directory.

## File Inventory and Schema Inspection

The following files were inspected in the `data/raw/olist/` directory. No data cleaning or transformations have been performed yet.

### 1. olist_customers_dataset.csv
- **Rows**: 99,441
- **Columns**: 5
- **Schema**: `customer_id`, `customer_unique_id`, `customer_zip_code_prefix`, `customer_city`, `customer_state`

### 2. olist_geolocation_dataset.csv
- **Rows**: 1,000,163
- **Columns**: 5
- **Schema**: `geolocation_zip_code_prefix`, `geolocation_lat`, `geolocation_lng`, `geolocation_city`, `geolocation_state`

### 3. olist_orders_dataset.csv
- **Rows**: 99,441
- **Columns**: 8
- **Schema**: `order_id`, `customer_id`, `order_status`, `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_estimated_delivery_date`

### 4. olist_order_items_dataset.csv
- **Rows**: 112,650
- **Columns**: 7
- **Schema**: `order_id`, `order_item_id`, `product_id`, `seller_id`, `shipping_limit_date`, `price`, `freight_value`

### 5. olist_order_payments_dataset.csv
- **Rows**: 103,886
- **Columns**: 5
- **Schema**: `order_id`, `payment_sequential`, `payment_type`, `payment_installments`, `payment_value`

### 6. olist_order_reviews_dataset.csv
- **Rows**: 99,224
- **Columns**: 7
- **Schema**: `review_id`, `order_id`, `review_score`, `review_comment_title`, `review_comment_message`, `review_creation_date`, `review_answer_timestamp`

### 7. olist_products_dataset.csv
- **Rows**: 32,951
- **Columns**: 9
- **Schema**: `product_id`, `product_category_name`, `product_name_lenght`, `product_description_lenght`, `product_photos_qty`, `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`

### 8. olist_sellers_dataset.csv
- **Rows**: 3,095
- **Columns**: 4
- **Schema**: `seller_id`, `seller_zip_code_prefix`, `seller_city`, `seller_state`

### 9. product_category_name_translation.csv
- **Rows**: 71
- **Columns**: 2
- **Schema**: `product_category_name`, `product_category_name_english`

## Validation
- All 9 expected CSV files from the Olist dataset are present.
- The row counts match the expected sizes for the public Kaggle dataset.
- Schemas align with the `docs/03_data/data_dictionary.md` definitions.

*Note: Proceeding to Module 4 (Data Cleaning & Preparation) requires explicit authorization.*
