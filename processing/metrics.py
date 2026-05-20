import pandas as pd
import os
import numpy as np
from ingestion.config import SILVER_PATH, TICKERS

RISK_FREE_RATE = 0.02 / 252  # 2% annual, converted to daily


def calculate_metrics(ticker: str, df: pd.DataFrame) -> dict:
    """
    Calculates financial risk metrics for a given ticker.
    Receives a DataFrame of log-returns and returns a dict with one row of metrics.
    """
    df = df.sort_values("Date")
    returns = df["log_return"]

    # Historical VaR: worst loss not exceeded 95%/99% of the time
    var_95 = returns.quantile(0.05)
    var_99 = returns.quantile(0.01)

    # Annualized volatility: daily std scaled by sqrt of trading days per year
    volatility = returns.std() * np.sqrt(252)

    # Sharpe ratio: excess return over risk-free rate per unit of risk
    sharpe = (returns.mean() - RISK_FREE_RATE) / volatility

    # Maximum drawdown: largest peak-to-trough decline in cumulative returns
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.cummax()
    max_drawdown = (cumulative / rolling_max - 1).min()

    return {
        "ticker": ticker,
        "var_95": var_95,
        "var_99": var_99,
        "volatility": volatility,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
    }


def run() -> None:
    """Calculates metrics for all tickers and saves to silver layer."""
    os.makedirs(SILVER_PATH, exist_ok=True)

    returns = pd.read_parquet(os.path.join(SILVER_PATH, "returns.parquet"))
    returns["Date"] = pd.to_datetime(returns["Date"])

    rows = [
        calculate_metrics(ticker, returns[returns["ticker"] == ticker])
        for ticker in TICKERS
    ]

    metrics = pd.DataFrame(rows)
    metrics.to_parquet(
        os.path.join(
            SILVER_PATH,
            "metrics.parquet"),
        index=False)
    print(f"Metrics saved: {len(metrics)} rows.")
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    run()
