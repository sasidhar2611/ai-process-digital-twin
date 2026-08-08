# Decisions Log

## Module 1
- Initialized standard repository structure.
- Created virtual environment and Git repository.
- Decided on strict module-by-module architecture strategy.
- Created public GitHub repository and established local-to-remote tracking, ensuring raw datasets are excluded.

## Module 4.1
- Decided to create a strict immutable Python data loading layer for raw datasets.
- Decided to add pandas to the requirements to handle CSV loading securely.
- Tests actively enforce file immutability using MD5 hashes and file stat modification checks.

## Module 2
- Selected Olist Brazilian E-Commerce dataset as the primary data source.
- Decided to synthesize internal warehouse timestamps and resource data using `order_id` as the primary linkage key.
- Established Lognormal stochastic processing based on real product dimensions for synthetic operations.
