import pandas as pd
import os
import numpy as np
from ingestion.config import BRONZE_PATH, SILVER_PATH, TICKERS


def calculate_returns(ticker: str) -> pd.DataFrame:
    """
    Calculates log-return for a given ticker.
    Returns a DataFrame with 'Date' and 'log_return' columns.
    """
    file_path = os.path.join(BRONZE_PATH, f"{ticker}.parquet")
    df = pd.read_parquet(file_path)

    # Ensure 'Date' is datetime and sort by date
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)

    # Calculate log-returns: log(Close_t / Close_{t-1})
    df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))

    df["ticker"] = ticker

    # Keep only relevant columns
    return df[["Date", "ticker", "Close", "log_return"]].dropna()


def run() -> None:
    """Calculates returns for all tickers and saves to silver layer."""

    os.makedirs(SILVER_PATH, exist_ok=True)
    all_returns = pd.concat([calculate_returns(ticker)
                            for ticker in TICKERS], ignore_index=True)

    # Save to silver layer
    silver_path = os.path.join(SILVER_PATH, "returns.parquet")
    all_returns.to_parquet(silver_path, index=False)

    print(f"Returns saved: {len(all_returns)} rows.")


if __name__ == "__main__":
    run()
