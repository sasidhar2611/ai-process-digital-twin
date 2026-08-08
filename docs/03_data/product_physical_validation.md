# Product Physical Data Validation Report

## Overview
This document summarizes the physical characteristics (weight, dimensions) of the Olist product dataset. These fields are crucial for the future digital-twin model to simulate warehouse picking/packing complexity and capacity constraints.

**Data Source & Units:**
- Weight (`product_weight_g`): Grams (REAL OBSERVED DATA)
- Dimensions (`product_length_cm`, `product_height_cm`, `product_width_cm`): Centimeters (REAL OBSERVED DATA)

## 1. Completeness
| Metric | Value |
|--------|-------|
| Total Products | 32,951 |
| Complete Physical Records | 32,949 |
| Incomplete Records | 2 |
| Completeness % | 99.99% |

**Conclusion**: The physical dataset is nearly perfect. Only 2 products lack physical characteristics.

## 2. Basic Validity
| Field | Zeros | Negatives | Missing | Classification |
|-------|-------|-----------|---------|----------------|
| `product_weight_g` | 4 | 0 | 2 | `REQUIRES_DOMAIN_VALIDATION` (Zero weight) |
| `product_length_cm` | 0 | 0 | 2 | `VALID` |
| `product_height_cm` | 0 | 0 | 2 | `VALID` |
| `product_width_cm` | 0 | 0 | 2 | `VALID` |

**Observations**:
- There are no negative physical values.
- 4 products have a reported weight of `0g`, which is physically impossible. This suggests either a data-entry default or a digital/intangible product. These should be treated as missing or requiring domain validation.
- All dimensions are strictly strictly greater than zero.

## 3. Distribution Characteristics
Descriptive statistics based on valid records (N=32,949).

| Field | Min | Median (P50) | Mean | Max |
|-------|-----|--------------|------|-----|
| Weight (g) | 0.0 | 700.0 | 2276.5 | 40,425.0 |
| Length (cm) | 7.0 | 25.0 | 30.8 | 105.0 |
| Height (cm) | 2.0 | 13.0 | 16.9 | 105.0 |
| Width (cm) | 6.0 | 20.0 | 23.2 | 118.0 |

**Percentiles Details:**
- **Weight**: P05=105g, P95=10,850g. The vast majority of items are under 11kg.
- **Length**: P05=16cm, P95=65cm.

## 4. Derived Analytical Volume
A derived volume calculation (`volume_cm3 = length * height * width`) was performed purely for analytical context.
**Note: This is DERIVED DATA and will not be written into the raw standardized dataset.**

| Metric | Value |
|--------|-------|
| Min Volume | 168 cm³ |
| Median Volume | 6,840 cm³ |
| Mean Volume | 16,564 cm³ |
| Max Volume | 296,208 cm³ (~296 Liters) |

## 5. Outlier Analysis & Plausibility
Statistical outliers were detected using the IQR method (1.5 * IQR above Q3).

| Field | IQR Upper Bound | Statistical Outliers | Plausibility |
|-------|-----------------|----------------------|--------------|
| Weight | 4,300g | 4,551 (13.8%) | Plausible. Large items (e.g., furniture, appliances) exist in Olist. |
| Length | 68.0cm | 1,380 (4.2%) | Plausible. Max length is 105cm. |
| Volume | 41,880cm³ | 3,262 (9.9%) | Plausible. Max volume is ~296L (e.g., a 105x105x26cm box). |

**Conclusion**: The statistical outliers in the right tail are heavily right-skewed but represent physically possible items. They are `STATISTICAL OUTLIERS` but NOT `PHYSICAL INVALIDITY`. Do not drop them.

## 6. Digital-Twin Relevance
The validated physical fields are fundamental to downstream process modeling:
- **Picking Complexity (FUTURE ASSUMPTION)**: Heavier and larger items (e.g., >20kg or >100cm) may require two-person picking or specialized handling equipment (forklifts).
- **Packing Complexity (FUTURE ASSUMPTION)**: Fragile or oversized items require specific box sizes and take longer to pack.
- **Capacity Constraints (FUTURE ASSUMPTION)**: A warehouse station or delivery truck has finite volumetric (`volume_cm3`) and weight (`product_weight_g`) capacities.

None of these relationships (e.g., time-per-gram) are established in the dataset itself. They will be synthesized in later modules.
