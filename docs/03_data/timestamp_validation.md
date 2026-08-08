# Timestamp Validation Report

## Overview
This document summarizes the temporal integrity validation of the Olist dataset. The goal is to identify missing timestamps, chronological anomalies, and relationship inconsistencies without mutating or dropping records.

## Analyzed Fields
**Orders:**
- `order_purchase_timestamp`
- `order_approved_at`
- `order_delivered_carrier_date`
- `order_delivered_customer_date`
- `order_estimated_delivery_date`

**Order Items:**
- `shipping_limit_date`

## 1. Missingness Analysis
| Field | Missing Count | Missing Percentage |
|-------|---------------|--------------------|
| `order_purchase_timestamp` | 0 | 0.00% |
| `order_approved_at` | 160 | 0.16% |
| `order_delivered_carrier_date` | 1,783 | 1.79% |
| `order_delivered_customer_date`| 2,965 | 2.98% |
| `order_estimated_delivery_date`| 0 | 0.00% |
| `shipping_limit_date` | 0 | 0.00% |

## 2. Chronological Rules Validation
| Rule | Description | Evaluated | Passed | Failed | Missing/Unavail | Fail Rate |
|------|-------------|-----------|--------|--------|-----------------|-----------|
| Rule A | purchase <= approved | 99,281 | 99,281 | 0 | 160 | 0.00% |
| Rule B | approved <= delivered_carrier | 97,644 | 96,285 | 1,359 | 1,797 | 1.39% |
| Rule C | delivered_carrier <= delivered_customer | 96,475 | 96,452 | 23 | 2,966 | 0.02% |
| Rule D | purchase <= delivered_customer | 96,476 | 96,476 | 0 | 2,965 | 0.00% |
| Rule E | delivered_customer <= estimated_delivery | 96,476 | 88,649 | 7,827 | 2,965 | 8.11% |
| Item A | approved <= shipping_limit | 112,635 | 112,508 | 127 | 15 | 0.11% |

## 3. Order Status Context (Expected Missingness)
Missing delivery timestamps closely align with `order_status`. Delivery dates are *expected* to be missing for incomplete statuses.
- `shipped`: 1,107 records (all missing delivery date - expected, transit phase)
- `canceled`: 625 records (619 missing delivery date - expected)
- `unavailable`: 609 records (all missing delivery date - expected)
- `invoiced`/`processing`: 615 records (all missing delivery date - expected)
- `delivered`: 96,478 records (Only 8 missing delivery dates - true anomaly)

## 4. Date Ranges
- `order_purchase_timestamp`: 2016-09-04 to 2018-10-17
- `order_approved_at`: 2016-09-15 to 2018-09-03
- `order_delivered_carrier_date`: 2016-10-08 to 2018-09-11
- `order_delivered_customer_date`: 2016-10-11 to 2018-10-17
- `order_estimated_delivery_date`: 2016-09-30 to 2018-11-12
- `shipping_limit_date`: 2016-09-19 to 2020-04-09 (Max date looks suspicious as purchases stop in 2018)

## 5. Business Interpretation & Anomalies
- **Rule B Failures (1.39%)**: 1,359 orders were logged as handed to the carrier *before* payment was approved. This may indicate asynchronous batch processing or deferred payment approvals.
- **Rule E Failures (8.11%)**: 7,827 orders were delivered *after* the estimated delivery date, indicating late deliveries. This is a business metric, not a data error.
- **`order_approved_at` semantics**: This is the REAL payment approval timestamp. It is NOT the physical warehouse-arrival timestamp. For the digital twin simulation, it may act as the real demand anchor, but assuming warehouse work begins exactly at this timestamp is a modeling assumption.
