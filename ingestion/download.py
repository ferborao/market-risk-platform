import os
import pandas as pd
import yfinance as yf
from ingestion.config import TICKERS, BRONZE_PATH


def get_last_date(ticker: str) -> pd.Timestamp | None:
    """
    Returns the most recent date recorded for a ticker.
    Returns None if no file exists yet (first download).
    """
    file_path = os.path.join(BRONZE_PATH, f"{ticker}.parquet")

    if not os.path.exists(file_path):
        return None

    df = pd.read_parquet(file_path)

    if df.empty:
        return None

    # Normalize column name — yfinance may save as 'Datetime' or 'Date'
    if "Datetime" in df.columns:
        df.rename(columns={"Datetime": "Date"}, inplace=True)

    return pd.to_datetime(df["Date"].max())


def download_ticker(ticker: str) -> None:
    """
    Downloads daily historical data for a ticker incrementally.
    - First run: downloads 5 years of historical data
    - Subsequent runs: downloads only from the last recorded date onwards
    """
    file_path = os.path.join(BRONZE_PATH, f"{ticker}.parquet")
    last_date = get_last_date(ticker)
    today = pd.Timestamp.today().normalize()

    # If the file was already checked today, skip — avoids redundant API calls
    # on weekends/holidays where there's no new trading data.
    if last_date is not None:
        mtime = pd.Timestamp.fromtimestamp(
            os.path.getmtime(file_path)).normalize()
        if mtime >= today:
            print(f"{ticker}: already up to date.")
            return

    if last_date is None:
        # First download: start from 5 years ago
        start_date = today - pd.DateOffset(years=5)
    else:
        # Incremental: start from the day after the last recorded date
        start_date = last_date + pd.Timedelta(days=1)

    # Normalize to midnight so date comparisons work without time component
    end_date = today

    # Nothing to download if already up to date
    if start_date >= end_date:
        print(f"{ticker}: already up to date.")
        return

    print(
        f"{ticker}: downloading from {
            start_date.date()} to {
            end_date.date()}...")

    # auto_adjust=True returns prices adjusted for dividends and stock splits
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True)
    assert data is not None

    if data.empty:
        print(f"{ticker}: no data returned.")
        return

    # Reset index to convert date from index to a regular column before saving
    data.reset_index(inplace=True)

    # Flatten MultiIndex columns returned by yfinance (e.g. ('Close',
    # 'BBVA.MC') -> 'Close')
    data.columns = [
        col[0] if isinstance(
            col,
            tuple) else col for col in data.columns]

    # yfinance may return 'Datetime' instead of 'Date' depending on version
    if "Datetime" in data.columns:
        data.rename(columns={"Datetime": "Date"}, inplace=True)

    if last_date is not None:
        new_rows = data[pd.to_datetime(data["Date"]) > last_date]
        if new_rows.empty:
            # Touch file so next run today skips the API call
            os.utime(file_path, None)
            print(f"{ticker}: already up to date.")
            return
        # Append new rows to existing data to preserve full history
        existing = pd.read_parquet(file_path)
        if "Datetime" in existing.columns:
            existing.rename(columns={"Datetime": "Date"}, inplace=True)
        data = pd.concat([existing, new_rows], ignore_index=True)

    data.to_parquet(file_path, index=False)
    print(f"{ticker}: saved {len(data)} rows to {file_path}.")


def run() -> None:
    """Runs incremental ingestion for all tickers."""
    os.makedirs(BRONZE_PATH, exist_ok=True)
    for ticker in TICKERS:
        download_ticker(ticker)


if __name__ == "__main__":
    run()
