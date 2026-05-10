import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = "/market_risk_dbt/dev.duckdb"
RETURNS_PATH = "data/silver/returns.parquet"

st.set_page_config(page_title="Market Risk Dashboard", layout="wide")
st.title("Market Risk Dashboard")

conn = duckdb.connect(DATA_PATH, read_only=True)

metrics = conn.execute("SELECT * FROM mart_risk_metrics").df()
correlations = conn.execute("SELECT * FROM mart_correlations").df()
returns = pd.read_parquet(RETURNS_PATH)