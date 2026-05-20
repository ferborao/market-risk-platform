import os

TICKERS = [
    "BBVA.MC", "SAN.MC", "CABK.MC",
    "JPM", "GS",
    "AAPL", "MSFT",
    "REP.MC", "XOM",
    "SPY",
]

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BRONZE_PATH = os.path.join(_PROJECT_ROOT, "data", "bronze")
SILVER_PATH = os.path.join(_PROJECT_ROOT, "data", "silver")
