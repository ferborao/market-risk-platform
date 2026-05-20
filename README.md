# Market Risk Data Platform

End-to-end market risk data platform processing real equity portfolio data with regulatory-grade risk metrics. Built as part of a Data Engineering portfolio targeting fintech and digital banking roles.

## Overview

Batch pipeline that ingests daily market data for a 10-ticker equity portfolio, calculates Basel-standard risk metrics (VaR, volatility, Sharpe ratio, maximum drawdown), and exposes the results through an interactive dashboard.

## Architecture
yfinance API → Bronze (Parquet) → Silver (Parquet) → Gold (DuckDB) → Streamlit Dashboard

Medallion architecture with three layers:
- **Bronze**: Raw daily OHLCV data, incremental ingestion, append-only
- **Silver**: Log-returns, risk metrics and correlation matrix
- **Gold**: dbt models exposed via DuckDB for analytical consumption

## Stack

| Layer | Technology |
|---|---|
| Ingestion | Python, yfinance |
| Processing | Python, Pandas, NumPy |
| Transformation | dbt, DuckDB |
| Orchestration | Apache Airflow |
| Infrastructure | Terraform |
| Dashboard | Streamlit, Plotly |
| CI/CD | GitHub Actions |

## Portfolio

10-ticker equity mix covering Spanish banking, global banking, tech, energy and a reference index:

`BBVA.MC` · `SAN.MC` · `CABK.MC` · `JPM` · `GS` · `AAPL` · `MSFT` · `REP.MC` · `XOM` · `SPY`

## Project Structure
market-risk-platform/
├── ingestion/          # Bronze layer: incremental yfinance download + validation
├── processing/         # Silver layer: log-returns, risk metrics, correlations
├── market_risk_dbt/    # Gold layer: dbt models over DuckDB
├── orchestration/      # Airflow DAG orchestrating the full pipeline
├── infrastructure/     # Terraform local infrastructure
├── dashboard/          # Streamlit portfolio risk dashboard
└── tests/              # Unit tests

## Setup

```bash
git clone https://github.com/ferborao/market-risk-platform.git
cd market-risk-platform

python3 -m venv .venv
source .venv/bin/activate

pip install dbt-core==1.9.0 dbt-duckdb==1.9.0 yfinance pandas pyarrow numpy duckdb streamlit plotly
pip install apache-airflow==2.9.3 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.12.txt"

pip install -e .
```

## Pipeline

Run the full pipeline manually:

```bash
# Ingest Bronze layer
python ingestion/download.py

# Validate data quality
python ingestion/validate.py

# Compute Silver metrics
python processing/returns.py
python processing/metrics.py
python processing/correlations.py

# Build Gold layer
cd market_risk_dbt && dbt run && dbt test
```

Or trigger the Airflow DAG:

```bash
export AIRFLOW_HOME=~/market-risk-platform/orchestration
airflow standalone
airflow dags trigger market_risk_pipeline
```

## Risk Metrics

| Metric | Description |
|---|---|
| VaR 95% / 99% | Historical Value at Risk (Basel standard, 252-day window) |
| Volatility | Annualized historical volatility (daily std × √252) |
| Sharpe Ratio | Excess return over 2% risk-free rate per unit of volatility |
| Max Drawdown | Largest peak-to-trough decline in cumulative returns |

## Dashboard

```bash
cd market-risk-platform
streamlit run dashboard/app.py
```

Open http://localhost:8501