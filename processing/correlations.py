from ingestion.config import SILVER_PATH
import pandas as pd
import os

def compute_correlations():
    """
    Compute the correlation matrix for the stock returns and save it as a CSV file.
    """

    # Load the stock returns data
    returns_path = os.path.join(SILVER_PATH, "returns.parquet")
    returns_df = pd.read_parquet(returns_path)

    pivoted_returns_df = returns_df.pivot(index='Date', columns='ticker', values='log_return')

    # Compute the correlation matrix
    correlation_matrix = pivoted_returns_df.corr()

    # Save the correlation matrix to a CSV file
    correlation_path = os.path.join(SILVER_PATH, "correlations.parquet")
    correlation_matrix.to_parquet(correlation_path)

def run():
    compute_correlations()
    print("Correlation matrix computed and saved.") 

if __name__ == "__main__":
    run()