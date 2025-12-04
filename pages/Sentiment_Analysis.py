import streamlit as st
from transformers import pipeline
from utils.loader import load_transactions
import pandas as pd

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

# -----------------------------
# Sentiment for transaction descriptions
# -----------------------------
st.subheader("💰 Financial Sentiment for Transactions")
st.info(
    "This section uses a rule-based approach. "
    "Sentiment is determined by the transaction amount: Positive for credits, Negative for debits."
)

df = load_transactions()


# Add sentiment based on Amount
@st.cache_data
def add_sentiment(df):
    # Positive amount = POSITIVE sentiment, Negative amount = NEGATIVE sentiment
    df["Sentiment"] = df["Amount"].apply(lambda x: "POSITIVE" if x >= 0 else "NEGATIVE")
    df["Sentiment Score"] = 1.0  # Score is 1.0 because this is a deterministic rule
    return df


df = add_sentiment(df)


# -----------------------------
# Filters (date & row count)
# -----------------------------
st.write("### 🔎 Filter Transactions")

col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input("From:", df["Posting Date"].min())

with col2:
    end_date = st.date_input("To:", df["Posting Date"].max())

with col3:
    limit = st.number_input("Show last N rows:", min_value=5, max_value=200, value=20)

# Filter by date range
df["Posting Date"] = pd.to_datetime(df["Posting Date"], errors="coerce")
filtered = df[
    (df["Posting Date"] >= pd.Timestamp(start_date))
    & (df["Posting Date"] <= pd.Timestamp(end_date))
]

# Show limited rows
st.dataframe(
    filtered[["Posting Date", "Description", "Amount", "Sentiment", "Sentiment Score"]]
    .sort_values("Posting Date", ascending=False)
    .head(limit)
)
