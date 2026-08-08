# Duplicate & Key Validation Report

## Overview
This document summarizes the identity and uniqueness characteristics of the Olist dataset. The goal is to determine primary keys, composite keys, and explicitly identify structural relationships or unexpected duplicates without mutating or dropping records.

## 1. Full Row Duplicates
| Dataset | Total Rows | Full Row Duplicates | Duplicate % | Classification |
|---------|------------|---------------------|-------------|----------------|
| `customers` | 99,441 | 0 | 0.00% | `NO_DUPLICATE` |
| `orders` | 99,441 | 0 | 0.00% | `NO_DUPLICATE` |
| `order_items` | 112,650 | 0 | 0.00% | `NO_DUPLICATE` |
| `products` | 32,951 | 0 | 0.00% | `NO_DUPLICATE` |
| `sellers` | 3,095 | 0 | 0.00% | `NO_DUPLICATE` |
| `order_payments` | 103,886 | 0 | 0.00% | `NO_DUPLICATE` |
| `order_reviews` | 99,224 | 0 | 0.00% | `NO_DUPLICATE` |
| `product_category_translation` | 71 | 0 | 0.00% | `NO_DUPLICATE` |
| `geolocation` | 1,000,163 | 261,831 | 26.18% | `FULL_ROW_DUPLICATE` |

*Note: The `geolocation` dataset has a high percentage of full-row duplicates, likely due to multiple coordinates being recorded for the same zip code prefix.*

## 2. Primary & Composite Key Analysis

### 2.1 Unique Keys
| Dataset | Key Field | Valid Rows | Unique Count | Classification |
|---------|-----------|------------|--------------|----------------|
| `orders` | `order_id` | 99,441 | 99,441 | `UNIQUE` |
| `customers` | `customer_id` | 99,441 | 99,441 | `UNIQUE` |
| `products` | `product_id` | 32,951 | 32,951 | `UNIQUE` |
| `sellers` | `seller_id` | 3,095 | 3,095 | `UNIQUE` |
| `translation` | `product_category_name` | 71 | 71 | `UNIQUE` |

### 2.2 Composite Keys
| Dataset | Composite Key | Valid Rows | Unique Count | Classification |
|---------|---------------|------------|--------------|----------------|
| `order_items` | `order_id` + `order_item_id` | 112,650 | 112,650 | `COMPOSITE_KEY_VALID` |
| `order_payments`| `order_id` + `payment_sequential` | 103,886 | 103,886 | `COMPOSITE_KEY_VALID` |

### 2.3 Expected Repeating Relationships
| Dataset | Key Field | Unique Count | Duplicate Count | Max Frequency |
|---------|-----------|--------------|-----------------|---------------|
| `customers` | `customer_unique_id` | 96,096 | 3,345 | 17 |
| `orders` | `customer_id` | 99,441 | 0 | 1 |
| `order_items` | `order_id` | 98,666 | 13,984 | 21 |
| `order_payments`| `order_id` | 99,440 | 4,446 | 29 |
| `order_reviews` | `order_id` | 98,673 | 551 | 3 |
| `geolocation` | `geolocation_zip_code_prefix`| 19,015 | 981,148 | 1,146 |

**Observations on Relationships:**
- **Customer Identity:** `customer_id` is perfectly unique to an order (1:1), while `customer_unique_id` identifies the actual human buyer across multiple orders. Thus, `customer_id` acts as an order-token, not a person-token.
- **Order Items:** The composite key `order_id` + `order_item_id` is perfectly unique. The `order_item_id` acts as a 1-based sequential index per order (Min: 1, Max: 21).

## 3. Unexpected Anomalies

### 3.1 Review ID Duplicates
- **Key**: `review_id` in `order_reviews`
- **Result**: `UNEXPECTED_DUPLICATE`
- **Details**: 814 duplicate `review_id` values exist (max frequency of 3).
- **Interpretation**: A single review might be mapped to multiple orders (e.g., if a customer buys multiple orders simultaneously and submits one review for all), or it's a structural glitch in data collection.

## 4. Treatment Recommendations

1. **Do Not Drop Row Duplicates in Geolocation**: The 26% duplicate rows in `geolocation` likely represent differing bounding box coordinates rounded or recorded redundantly. If aggregated to a zip-code level later, taking a median/mean coordinate is safer than randomly dropping rows.
2. **Handle `review_id` Duplicates Carefullly**: Since `review_id` is not perfectly unique, it cannot be used as a primary key for JOINs without handling the many-to-many relationship with orders.
3. **Use Composite Keys for Transactions**: Always use `order_id` + `order_item_id` for item-level granularity, and `order_id` + `payment_sequential` for payments.
4. **Distinguish Customer IDs**: Never join on `customer_id` if the goal is customer-lifetime-value tracking. Use `customer_unique_id`.
