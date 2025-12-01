import streamlit as st
from transformers import pipeline
from utils.loader import load_transactions
import pandas as pd

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

# -----------------------------
# Load HuggingFace model once
# -----------------------------
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

model = load_model()

# -----------------------------
# UI
# -----------------------------
st.title("💭 Sentiment Analysis (HuggingFace)")

st.subheader("📝 Enter text to analyze sentiment:")
text = st.text_area("Type something...", height=150)

# -----------------------------
# Analyze single text input
# -----------------------------
if st.button("Analyze"):
    if text.strip():
        result = model(text)[0]
        label = result["label"]
        score = result["score"]

        emoji = "😊" if label == "POSITIVE" else "😞"

        st.success(f"**Sentiment:** {label} {emoji}")
        st.write(f"Confidence: `{score:.3f}`")

    else:
        st.warning("Please enter text.")

st.markdown("---")

# -----------------------------
# Sentiment for transaction descriptions
# -----------------------------
st.subheader("📦 Sentiment for Transaction Descriptions")

df = load_transactions()

# Add sentiment using model
@st.cache_data
def add_sentiment(df):
    sentiments = []
    scores = []
    for text in df["Description"].astype(str):
        res = model(text)[0]
        sentiments.append(res["label"])
        scores.append(res["score"])
    df["Sentiment"] = sentiments
    df["Sentiment Score"] = scores
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
    (df["Posting Date"] >= pd.Timestamp(start_date)) &
    (df["Posting Date"] <= pd.Timestamp(end_date))
]

# Show limited rows
st.dataframe(
    filtered[["Posting Date", "Description", "Amount", "Sentiment", "Sentiment Score"]]
        .sort_values("Posting Date", ascending=False)
        .head(limit)
)
