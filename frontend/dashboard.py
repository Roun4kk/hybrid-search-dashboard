import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Hybrid Search Dashboard", layout="wide")

st.title("Hybrid Search KPI Dashboard")

conn = sqlite3.connect("data/metrics/search_logs.db")

df = pd.read_sql_query("SELECT * FROM search_logs", conn)

conn.close()

# ---- Metrics ----

col1, col2 = st.columns(2)

col1.metric("Total Queries", len(df))

zero_results = len(df[df["result_count"] == 0])

col2.metric("Zero Result Queries", zero_results)

st.divider()

# ---- Top Queries ----

st.subheader("Top Queries")

top_queries = df["query"].value_counts().reset_index()
top_queries.columns = ["query", "count"]

st.dataframe(top_queries)

st.bar_chart(top_queries.set_index("query"))

st.divider()

# ---- Recent Searches ----

st.subheader("Recent Searches")

recent = df.sort_values("timestamp", ascending=False).head(10)

st.dataframe(recent)