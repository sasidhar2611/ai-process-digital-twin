# Data Lineage

This document traces the flow of data through the AI-Process-Digital-Twin architecture, explicitly defining the distinction between Real, Derived, Synthetic, and Analytical data.

## Lineage Diagram

```
[REAL DATA] (Olist CSVs)
       ↓
(RawDataLoader)
       ↓
[DERIVED DATA] (Standardized/Imputed DataFrames)
       ↓
(DataValidators)
       ↓
[DERIVED DATA] (Processed Parquet Files)
       ↓
(Synthetic Data Generator & Config)
       ↓
[SYNTHETIC DATA] (Simulated Operational Timelines)
       ↓
(KPI Extractor)
       ↓
[ANALYTICAL RESULTS] (Aggregated JSONs & Parquet Metrics)
       ↓
(Bottleneck Analyzer)
       ↓
[ANALYTICAL RESULTS] (Intervention Rankings)
```

## Data Definitions

### 1. REAL DATA
- **Definition**: The untainted, original records supplied by Olist.
- **Sources**: `olist_orders_dataset.csv`, `olist_order_items_dataset.csv`, `olist_products_dataset.csv`.
- **Content**: E-commerce demand, real approval timestamps, actual items, actual product categories, and real shipping states.

### 2. DERIVED DATA
- **Definition**: Real data that has been cleaned, typed, filtered, or imputed by the standardizer pipeline. It is not synthetic operationally, it is merely refined mathematically.
- **Sources**: Standardizer, Missing Data Handler.
- **Content**: Typed columns, imputed missing volumes/weights, dropped invalid orders, serialized Parquet data in `data/processed/`.

### 3. SYNTHETIC DATA
- **Definition**: The entirely fabricated warehouse operational event timeline built *on top of* the derived real data.
- **Sources**: Synthetic Generator.
- **Content**: Stage processing times, queue wait times, worker start/end timestamps, shift boundary logic, bottleneck buildup.

### 4. ANALYTICAL RESULTS
- **Definition**: Mathematical aggregations, KPIs, and algorithmic evaluations generated from evaluating the synthetic data.
- **Sources**: KPI Extractor, Bottleneck Analyzer.
- **Content**: Mean flow times, stage utilizations, P95 metrics, comparative ranking tables.
