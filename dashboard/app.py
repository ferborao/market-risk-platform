import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = "market_risk_dbt/dev.duckdb"
RETURNS_PATH = "data/silver/returns.parquet"

st.set_page_config(page_title="Market Risk Dashboard", layout="wide")
st.title("Market Risk Dashboard")

conn = duckdb.connect(DATA_PATH, read_only=True)

metrics = conn.execute("SELECT * FROM mart_risk_metrics").df()
correlations = conn.execute("SELECT * FROM mart_correlations").df()
returns = pd.read_parquet(RETURNS_PATH)

st.sidebar.header("Portfolio Filter")
selected_tickers = st.sidebar.multiselect(
    "Select tickers",
    options=metrics["ticker"].tolist(),
    default=metrics["ticker"].tolist()
)

filtered_metrics = metrics[metrics["ticker"].isin(selected_tickers)]
filtered_returns = returns[returns["ticker"].isin(selected_tickers)]

st.subheader("Risk Metrics Summary")

st.dataframe(filtered_metrics, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("VaR 95% by Ticker")
    fig_var = px.bar(
        filtered_metrics.sort_values("var_95"),
        x="ticker", y="var_95",
        color="risk_level",
        color_discrete_map={"High": "#ff4444", "Medium": "#ffaa00", "Low": "#44bb44"}
    )
    st.plotly_chart(fig_var, use_container_width=True)

with col2:
    st.subheader("Annualized Volatility by Ticker")
    fig_vol = px.bar(
        filtered_metrics.sort_values("volatility", ascending=False),
        x="ticker", y="volatility",
        color="risk_level",
        color_discrete_map={"High": "#ff4444", "Medium": "#ffaa00", "Low": "#44bb44"}
    )
    st.plotly_chart(fig_vol, use_container_width=True)

    st.subheader("Correlation Matrix")
    corr_pivot = correlations.pivot(index="ticker_a", columns="ticker_b", values="correlation")
    fig_corr = px.imshow(
        corr_pivot,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        text_auto=".2f"
    )
    fig_corr.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("Cumulative Returns")
    filtered_returns["Date"] = pd.to_datetime(filtered_returns["Date"])
    filtered_returns = filtered_returns.sort_values("Date")
    filtered_returns["cumulative_return"] = filtered_returns.groupby("ticker")["log_return"].cumsum()
    fig_returns = px.line(
        filtered_returns,
        x="Date", y="cumulative_return",
        color="ticker"
    )
    st.plotly_chart(fig_returns, use_container_width=True)