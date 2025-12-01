import pandas as pd
import re
import google.generativeai as genai
from utils.config import MODEL_NAME
import streamlit as st

@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def clean_data():
    df = pd.read_csv("data/raw_chase.csv")

    # fix hidden spaces
    df.columns = df.columns.str.strip()

    required = ["Details", "Posting Date", "Description", "Amount", "Balance"]
    df = df[required].copy()

    # fix date
    df["Posting Date"] = pd.to_datetime(
        df["Posting Date"], errors="coerce", infer_datetime_format=True
    )
    df = df.dropna(subset=["Posting Date"])

    df["Amount"] = (
        df["Amount"].astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["Description"] = df["Description"].astype(str).apply(
        lambda x: re.sub(r"\d+", "", x).strip()
    )

    # If already categorized, skip
    if "Category" in df and df["Category"].notna().all():
        df.to_csv("data/cleaned.csv", index=False)
        return df
def ai_batch_categorize(df):
    import json
    model = genai.GenerativeModel(MODEL_NAME)
    descriptions = df["Description"].tolist()

    prompt = f"""
Return a JSON array where each item is the category for the matching transaction.

Valid categories:
["Groceries","Dining","Coffee","Shopping","Transport","Travel","Health",
"Entertainment","Bills","Utilities","Education","Subscriptions","Income","Other"]

Descriptions:
{descriptions}

Respond ONLY with JSON. No explanation.
"""

    resp = model.generate_content(prompt)
    raw = resp.text.strip()

    # --- Clean AI formatting ---
    # Remove code fences like ```json ... ```
    if raw.startswith("```"):
        raw = raw.replace("```json", "", 1)
        raw = raw.replace("```", "")
        raw = raw.strip()

    # Remove stray backticks
    raw = raw.replace("```", "").strip()

    # Parse JSON
    try:
        categories = json.loads(raw)
    except Exception:
        raise ValueError(f"❌ Cleaned AI output is not valid JSON:\n{raw}")

    if len(categories) != len(df):
        raise ValueError(
            f"❌ AI returned {len(categories)} categories for {len(df)} rows"
        )

    df["Category"] = categories
    return df

    # AI category assignment
    df = ai_batch_categorize(df)
    df.to_csv("data/cleaned.csv", index=False)
    return df

