# Hybrid Trader

Hybrid Trader is a modular system for researching and running live crypto trading strategies.

## Features
- Pydantic-based configuration loaded from `.env` files
- Environment checks for Python version, required dependencies, and NTP clock sync
- Hive-style parquet folder scaffolding utilities
- Structured JSON logging with run manifest generation

## Setup
1. Ensure Python 3.10+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   or for development:
   ```bash
   pip install -e .
   ```
3. Copy `.env.example` to `.env` and adjust settings as needed

## Usage
Run foundational checks and generate a manifest:

```bash
python -m hybrid_trader
```

Further phases will add data ingestion, feature engineering, labeling, modeling, and execution logic.
