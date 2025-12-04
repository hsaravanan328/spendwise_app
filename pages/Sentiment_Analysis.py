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
    # Load a model trained for 3-class sentiment analysis (positive, neutral, negative)
    return pipeline(
        "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment"
    )

model = load_model()

# -----------------------------
# UI
# -----------------------------
st.title("💭 Sentiment Analysis")

st.subheader("📝 Analyze Custom Text")
st.info(
    "This section uses a RoBERTa model trained for 3-class sentiment analysis (Positive, Negative, Neutral)."
)
text = st.text_area(
    "Type something...",
    height=150,
    placeholder="Example: 'I am happy today!'",
)

# -----------------------------
# Analyze single text input
# -----------------------------
if st.button("Analyze Text"):
    if text.strip():
        result = model(text)[0]
        raw_label = result["label"]
        score = result["score"]

        # Map the model's raw output (e.g., 'LABEL_2') to a friendly name and emoji
        if raw_label == "LABEL_2":
            label = "POSITIVE"
            emoji = "😊"
        elif raw_label == "LABEL_0":
            label = "NEGATIVE"
            emoji = "😞"
        else:  # Assumes LABEL_1 or any other case is Neutral
            label = "NEUTRAL"
            emoji = "😐"

        st.success(f"**Sentiment:** {label} {emoji}")
        st.write(f"Confidence: `{score:.3f}`")

    else:
        st.warning("Please enter text.")

st.markdown("---")

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
