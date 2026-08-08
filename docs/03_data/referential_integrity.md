# Referential Integrity Validation Report

## Overview
This document summarizes the validation of referential integrity (foreign key relationships) across the Olist dataset. The goal is to verify that all cross-dataset references point to valid records and explicitly document any orphans or expected absences without modifying the raw data.

## 1. Core Foreign Key Relationships
The Olist dataset demonstrates exceptional referential integrity across all core operational tables.

| Relationship | Expected | Match Rate | Orphans | Classification |
|--------------|----------|------------|---------|----------------|
| `orders.customer_id` → `customers.customer_id` | `FOREIGN_KEY` | 100.0% | 0 | `VALID_MATCH` |
| `order_items.order_id` → `orders.order_id` | `FOREIGN_KEY` | 100.0% | 0 | `VALID_MATCH` |
| `order_items.product_id` → `products.product_id` | `FOREIGN_KEY` | 100.0% | 0 | `VALID_MATCH` |
| `order_items.seller_id` → `sellers.seller_id` | `FOREIGN_KEY` | 100.0% | 0 | `VALID_MATCH` |
| `order_payments.order_id` → `orders.order_id` | `FOREIGN_KEY` | 100.0% | 0 | `VALID_MATCH` |
| `order_reviews.order_id` → `orders.order_id` | `FOREIGN_KEY` | 100.0% | 0 | `VALID_MATCH` |

**Conclusion**: There are **zero** orphan records in the core operational relationships. Every item maps to a valid product, seller, and order. Every order maps to a valid customer.

## 2. Product Category Translation
| Relationship | Expected | Match Rate | Unmatched Categories | Missing Categories | Classification |
|--------------|----------|------------|----------------------|--------------------|----------------|
| `products.product_category_name` → `translation.product_category_name` | `TRANSLATION` | 98.11% | 13 (0.04%) | 610 | `UNTRANSLATED_CATEGORY` |

**Conclusion**: The translation dataset is a helper mapping, not a strict parent table. 
- 610 products intentionally lack a category string (`EXPECTED_ABSENCE`).
- 13 unique products possess a category string that simply does not appear in the translation dictionary (`UNTRANSLATED_CATEGORY`).
- These are NOT orphan products; they merely lack an English translation mapping.

## 3. Order Reviews Many-to-Many Relationship
While all `order_id` values in `order_reviews` validly map back to `orders`, the relationship between reviews and orders is **many-to-many**, not strictly one-to-one or one-to-many.

- **Orders with multiple reviews**: 547 orders have multiple distinct reviews associated with them (Max: 3 reviews per order).
- **Reviews mapping to multiple orders**: 789 single `review_id` values map to multiple distinct orders (Max: 3 orders per review).

**Interpretation**: A single customer purchasing multiple orders in the same cart/session likely received a single review prompt, mapping their one review payload to multiple distinct `order_id` records in the database.

## 4. Order Items Characteristics
- **Minimum items per order**: 1
- **Maximum items per order**: 21
- No orphan items exist.

## 5. Payments Characteristics
- All payment records map to valid orders.
- Orders may have multiple payment records (e.g., using a combination of a voucher and a credit card). This is entirely valid and structural, not an integrity violation.
