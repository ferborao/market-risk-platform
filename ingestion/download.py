import os
import pandas as pd
import yfinance as yf
from yfinance import ticker

TICKERS = [    
    "BBVA.MC", "SAN.MC", "CABK.MC",  
    "JPM", "GS",                        
    "AAPL", "MSFT",                     
    "REP.MC", "XOM",                   
    "SPY",                              
]

DATA_PATH = "data/bronze/"

def get_last_date(ticker: str) -> pd.Timestamp | None:
    file_path = os.path.join(DATA_PATH, f"{ticker}.parquet")
    if not os.path.exists(file_path):
        return None
    df = pd.read_parquet(file_path)
    if df.empty:
        return None
    return pd.to_datetime(df["Date"].max())


def download_ticker(ticker: str) -> None:
    file_path = os.path.join(DATA_PATH, f"{ticker}.parquet")
    last_date = get_last_date(ticker)

    if last_date is None:
        start_date = pd.Timestamp.today() - pd.DateOffset(years=5)
    else:
        start_date = last_date + pd.Timedelta(days=1)

    end_date = pd.Timestamp.today()

    if start_date >= end_date:
        print(f"{ticker}: already up to date.")
        return

    print(f"{ticker}: downloading from {start_date.date()} to {end_date.date()}...")
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    assert data is not None

    if data.empty:
        print(f"{ticker}: no data returned.")
        return

    data.reset_index(inplace=True)

    if last_date is not None:
        existing = pd.read_parquet(file_path)
        data = pd.concat([existing, data]).drop_duplicates(subset=["Date"])

    data.to_parquet(file_path, index=False)
    print(f"{ticker}: saved {len(data)} rows to {file_path}.")


def run() -> None:
    os.makedirs(DATA_PATH, exist_ok=True)
    for ticker in TICKERS:
        download_ticker(ticker)


if __name__ == "__main__":
    run()