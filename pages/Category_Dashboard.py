import streamlit as st
from utils.loader import load_transactions
import pandas as pd
import plotly.express as px

st.title("📊 Category Dashboard")

df = load_transactions()

cat = st.selectbox("Choose a category:", sorted(df["Category"].unique()))

filtered = df[df["Category"] == cat]

st.write(f"### Total in {cat}: **${filtered['Amount'].sum():,.2f}**")

fig = px.bar(
    filtered,
    x="Posting Date",
    y="Amount",
    title=f"{cat} Spending Over Time",
)
fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

st.write("### Recent Transactions")
num_rows = st.selectbox("Show last:", [5, 10, 20, 50], index=0)

st.dataframe(
    filtered.sort_values("Posting Date", ascending=False).head(num_rows)
)

