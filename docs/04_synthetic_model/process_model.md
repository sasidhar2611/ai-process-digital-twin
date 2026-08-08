# Operational Process Model

This document defines the exact process stages for the AI-Driven Process Digital Twin. The synthetic operational model mimics an e-commerce fulfillment warehouse based on Olist order data.

## Process Stages
The fulfillment process is modeled as a strict linear sequence of 5 stages. Each stage must logically complete before the next begins.

| Sequence | Stage Name | Description |
|----------|------------|-------------|
| 1 | PROCESSING | Digital routing, label generation, and order allocation to warehouse zones. |
| 2 | PICKING | Physical retrieval of items from storage by workers. |
| 3 | PACKING | Boxing and sealing items into shipping parcels. |
| 4 | SORTING | Categorizing packed parcels by carrier and delivery route. |
| 5 | DISPATCH | Loading parcels onto outbound carrier vehicles. |

## Sequence Logic
- A single Olist `order_id` flows sequentially through stages 1 to 5.
- Stage `N+1` cannot start until Stage `N` finishes.
- Missing intermediate stage skipping is NOT permitted unless defined by a specific exception rule (which is not currently assumed).

## Real Demand Anchor
The demand arrival anchor for the model is:
- **`order_approved_at`** (REAL DATA): This represents the payment approval timestamp. 
- **ASSUMPTION**: An order becomes eligible for warehouse processing exactly at its payment approval timestamp. It enters the queue for Stage 1 (PROCESSING) at this time. Orders missing an approval timestamp are excluded from the synthetic operational timeline.
