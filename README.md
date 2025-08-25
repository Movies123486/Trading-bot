# Hybrid Trader

Hybrid Trader is a modular trading system focused on realistic research and live operation for crypto markets.

## Phase 0 – Foundations

This repository currently contains the foundation utilities:

- Pydantic based configuration loaded from `.env`
- Environment checks for Python version, required dependencies and NTP clock sync
- Hive-style parquet folder scaffolding utilities
- Structured JSON logging with run manifest generation

Execute `python -m hybrid_trader` to run the checks and create a manifest.

Further phases will add data ingestion, feature engineering, labeling, modeling and execution logic.
