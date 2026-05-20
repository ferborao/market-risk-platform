import pytest
import pandas as pd
import numpy as np
from processing.metrics import calculate_metrics


def test_calculate_metrics_returns_correct_keys():
    """Metrics dict must contain all required keys."""
    df = pd.DataFrame({
        "Date": pd.date_range("2020-01-01", periods=300),
        "ticker": ["AAPL"] * 300,
        "log_return": np.random.normal(0.001, 0.02, 300)
    })
    result = calculate_metrics("AAPL", df)
    assert set(result.keys()) == {"ticker", "var_95", "var_99", "volatility", "sharpe", "max_drawdown"}


def test_var_95_less_than_var_99():
    """VaR 95% should be greater than VaR 99% (less negative)."""
    df = pd.DataFrame({
        "Date": pd.date_range("2020-01-01", periods=300),
        "ticker": ["AAPL"] * 300,
        "log_return": np.random.normal(0.001, 0.02, 300)
    })
    result = calculate_metrics("AAPL", df)
    assert result["var_95"] > result["var_99"]


def test_volatility_is_positive():
    """Volatility must always be positive."""
    df = pd.DataFrame({
        "Date": pd.date_range("2020-01-01", periods=300),
        "ticker": ["AAPL"] * 300,
        "log_return": np.random.normal(0.001, 0.02, 300)
    })
    result = calculate_metrics("AAPL", df)
    assert result["volatility"] > 0