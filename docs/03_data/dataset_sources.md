# Dataset Sources

## Primary Dataset Recommendation

**Recommended Dataset**: Olist Brazilian E-Commerce Public Dataset
**Source**: Kaggle (https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### Justification
The Olist dataset is the most comprehensive public e-commerce dataset available for order-level simulation. It provides a realistic foundation of ~100k real orders containing rich attributes:
- **Order timing**: Contains timestamp fields such as purchase, approval, and delivery.
- **Product details**: Contains physical dimensions (weight, length, height, width) which are excellent proxies for simulation mechanics like packing and picking effort.
- **Customer/Seller data**: Provides geographic distribution for logistical complexity.

### What is Available
The dataset provides files like:
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_products_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_sellers_dataset.csv`

### What is Missing
The dataset does NOT provide internal warehouse/fulfillment center operational details. Specifically, it lacks:
- Warehouse workers (IDs, counts, shifts, productivity)
- Stage workers and assignments
- Timestamps for internal stages: Picking, Packing, Sorting, Dispatch
- Queue lengths and stage capacity
- Resource utilization

### Alternatives Considered
1. **Instacart Market Basket Analysis Dataset**: Focuses heavily on market basket and product recommendations rather than fulfillment logistics and timestamps. Lacks order lifecycle details.
2. **UCI Online Retail Dataset**: Contains transactional data but lacks granular timestamping for fulfillment lifecycle and physical product dimensions needed for fulfillment simulation.

The Olist dataset is selected as the primary real data source because it uniquely provides both the logistical timestamps and product characteristics necessary to anchor our synthetic digital twin.
