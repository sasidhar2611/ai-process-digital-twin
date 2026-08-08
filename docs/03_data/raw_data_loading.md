# Raw Data Loading Strategy

## Purpose
The `RawDataLoader` class (`src/data/raw_data_loader.py`) provides a clean, reusable Python data-loading layer. It reads the raw Olist CSV files into structured Pandas DataFrames. It is designed as a foundational layer for all future cleaning and transformation modules.

## Raw Data Location
The raw datasets are strictly loaded from `data/raw/olist/`.

## Supported Datasets
The loader supports the core Olist datasets:
- `customers` (`olist_customers_dataset.csv`)
- `geolocation` (`olist_geolocation_dataset.csv`)
- `orders` (`olist_orders_dataset.csv`)
- `order_items` (`olist_order_items_dataset.csv`)
- `order_payments` (`olist_order_payments_dataset.csv`)
- `order_reviews` (`olist_order_reviews_dataset.csv`)
- `products` (`olist_products_dataset.csv`)
- `sellers` (`olist_sellers_dataset.csv`)
- `product_category_translation` (`product_category_name_translation.csv`)

## Loading Behavior
- Validates the existence of the expected data directory.
- Checks for the presence of the specific requested CSV file.
- Reads the raw CSV file directly into a Pandas DataFrame using default parsing logic.
- Returns the unadulterated DataFrame.

## Immutability Rule
**THIS IS CRITICAL:** The files inside `data/raw/olist/` must NEVER be modified by this loader.
The loader:
- Does NOT clean values.
- Does NOT rename columns.
- Does NOT convert business fields.
- Does NOT remove rows or duplicates.
- Does NOT fill missing values.
- Does NOT overwrite the raw files.
Its sole responsibility is *reading* the original source data reliably.

## Error Handling
- `ValueError` is raised if an invalid dataset logical name is requested.
- `FileNotFoundError` is raised if the target CSV file does not exist in the designated path.

## Test Approach
Unit tests are located in `tests/unit/test_raw_data_loader.py` and are executed using `pytest`.
Tests cover:
1. Custom directory initialization.
2. Verification of expected file detection.
3. Loading success and DataFrame validation.
4. Error handling for missing files or invalid names.
5. **Raw Data Protection Test**: Explicitly checks file size, modification timestamps, and MD5 hashes of the actual raw files before and after loading to guarantee immutability.
