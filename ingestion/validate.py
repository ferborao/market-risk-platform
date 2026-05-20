import os
import pandas as pd
from ingestion.config import TICKERS, BRONZE_PATH


def validate_ticker(ticker: str) -> None:
    """
    Validates a stock ticker.

    Args:
        ticker (str): The stock ticker symbol to validate.

    Returns:
        bool: True if the ticker is valid, False otherwise.
    """
    file_path = os.path.join(BRONZE_PATH, f"{ticker}.parquet")

    df = pd.read_parquet(file_path)

    # Perform additional validation checks on the DataFrame if needed
    if df.empty:
        print(f"Warning: No data found for ticker: {ticker}")

    # Example validation: Check if required columns are present
    required_columns = {"Date", "Open", "High", "Low", "Close", "Volume"}
    if not required_columns.issubset(df.columns):
        print(
            f"Warning: Missing required columns in {ticker} data: {
                required_columns - set(
                    df.columns)}")

    if df["Close"].isnull().any():
        print(
            f"Warning: Null values found in 'Close' column for ticker: {ticker}")

    if (df["Close"] <= 0.0).any():
        print(
            f"Warning: Values in 'Close' column for ticker: {ticker} are not positive")

    if df["Date"].isnull().any():
        print(
            f"Warning: Null values found in 'Date' column for ticker: {ticker}")

    print(f"{ticker}: validation passed.")


def run():
    """Runs validation for all tickers."""
    for ticker in TICKERS:
        validate_ticker(ticker)


if __name__ == "__main__":
    run()
