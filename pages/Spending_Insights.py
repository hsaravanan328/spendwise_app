'''
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_transactions

st.set_page_config(page_title="Spending Breakdown", layout="wide")
st.title("📊 Spending Breakdown")

# =============================
# Load Data
# =============================
df = load_transactions()
df["Posting Date"] = pd.to_datetime(df["Posting Date"], errors="coerce")

# =============================
# Date Filters
# =============================
st.subheader("🗓️ Filter by Date Range")

col1, col2 = st.columns(2)
min_date = df["Posting Date"].min()
max_date = df["Posting Date"].max()

with col1:
    start_date = st.date_input("Start Date", min_date)

with col2:
    end_date = st.date_input("End Date", max_date)

mask = (df["Posting Date"] >= pd.to_datetime(start_date)) & (
    df["Posting Date"] <= pd.to_datetime(end_date)
)
filtered_df = df[mask].copy()

st.write(f"### Showing transactions from **{start_date} → {end_date}**")
st.write(f"Total transactions: **{len(filtered_df)}**")

# =========================================================
# 0️⃣ CLEAN COLUMNS
# =========================================================

# Remove time from Posting Date
filtered_df["Posting Date"] = filtered_df["Posting Date"].dt.date

# Format Amount
filtered_df["Amount"] = filtered_df["Amount"].astype(float).round(2)

# Positive value for spending bucket logic
filtered_df["SpendPos"] = filtered_df["Amount"].abs()

# =========================================================
# UNIFIED BUCKET COLUMN (Fix KeyError)
# =========================================================

def bucketize(amount, detail):
    if detail == "CREDIT":
        return "Income"
    if amount < 10:
        return "Micro (<$10)"
    elif amount < 30:
        return "Small ($10–$30)"
    elif amount < 100:
        return "Medium ($30–$100)"
    elif amount < 300:
        return "Large ($100–$300)"
    else:
        return "Major (>$300)"

filtered_df["Bucket"] = filtered_df.apply(
    lambda row: bucketize(row["SpendPos"], row["Details"]), axis=1
)

# =============================
# 1️⃣ Spending Over Time Chart
# =============================
st.markdown("### 📈 Spending Over Time")

daily = (
    filtered_df.copy()
    .set_index(pd.to_datetime(filtered_df["Posting Date"]))
    .resample("D")["Amount"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily,
    x="Posting Date",
    y="Amount",
    title="Daily Spending Trend",
    markers=True,
)

fig.update_traces(line=dict(color="#4a74c9", width=3))
fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 2️⃣ WEEKDAY SPENDING HEATMAP
# =========================================================
st.subheader("📅 Weekly Spending Heatmap")

filtered_df["Weekday"] = pd.to_datetime(filtered_df["Posting Date"]).dt.day_name()

weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekday_summary = (
    filtered_df.groupby("Weekday")["SpendPos"]
    .sum()
    .reindex(weekday_order)
    .reset_index()
)

fig1 = px.imshow(
    [weekday_summary["SpendPos"]],
    labels=dict(x="Day of Week", color="Total Spend ($)"),
    x=weekday_summary["Weekday"],
    aspect="auto",
    color_continuous_scale="Blues",
)

fig1.update_layout(margin=dict(l=10, r=10, t=40, b=40))
st.plotly_chart(fig1, use_container_width=True)

st.write("### Weekday Summary")
st.dataframe(weekday_summary.rename(columns={"SpendPos": "Spending"}), hide_index=True)

# =========================================================
# 3️⃣ SPENDING BUCKETS (Only Spending, No Income)
# =========================================================

st.subheader("💵 Spending Buckets")

spend_df = filtered_df[filtered_df["Details"] == "DEBIT"].copy()
spend_df["Bucket"] = spend_df["SpendPos"].apply(
    lambda x: bucketize(x, "DEBIT")
)

bucket_summary = (
    spend_df.groupby("Bucket")["SpendPos"]
    .sum()
    .reset_index()
    .rename(columns={"SpendPos": "Total Spend"})
)

bucket_order = [
    "Micro (<$10)",
    "Small ($10–$30)",
    "Medium ($30–$100)",
    "Large ($100–$300)",
    "Major (>$300)",
]

bucket_summary["Bucket"] = pd.Categorical(bucket_summary["Bucket"], bucket_order)
bucket_summary = bucket_summary.sort_values("Bucket")

colors = ["#bcd4ff", "#8bb8ff", "#5e9bff", "#3b7aff", "#1e5fe0"]

fig2 = px.bar(
    bucket_summary,
    x="Bucket",
    y="Total Spend",
    text_auto=".2s",
    title="Spending by Amount Bucket",
    color="Bucket",
    color_discrete_sequence=colors,
)

fig2.update_layout(
    xaxis_title="Bucket",
    yaxis_title="Total Spend ($)",
)

st.plotly_chart(fig2, use_container_width=True)
st.write("### Bucket Breakdown")
st.dataframe(bucket_summary, hide_index=True)

# =============================
# 4️⃣ Detailed Table (Bucket colored)
# =============================

st.markdown("### 🧾 Detailed Transactions")

num_rows = st.slider("Rows to display:", 5, 50, 15)

# Remove Category column
table_df = filtered_df[
    ["Details", "Posting Date", "Description", "Amount", "Balance", "Bucket"]
].sort_values("Posting Date", ascending=False).head(num_rows)

# ----- Color map for buckets -----
bucket_colors = {
    "Income": "#b3e6b3",          # soft green
    "Micro (<$10)": "#e0ecff",    # very light blue
    "Small ($10–$30)": "#bfd6ff",  # light blue
    "Medium ($30–$100)": "#9abfff",  # mid blue
    "Large ($100–$300)": "#6f9dff",   # deeper blue
    "Major (>$300)": "#4666ff",    # strong indigo
}

def highlight_row(row):
    color = bucket_colors.get(row["Bucket"], "#ffffff")
    return [f"background-color: {color}; color:black;"] * len(row)

styled_table = table_df.style.apply(highlight_row, axis=1)

st.dataframe(styled_table, hide_index=True)
'''
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_transactions

st.set_page_config(page_title="Spending Breakdown", layout="wide")
st.title("📊 Spending Breakdown")

# =============================
# Load Data
# =============================
df = load_transactions()
df["Posting Date"] = pd.to_datetime(df["Posting Date"], errors="coerce")

# =============================
# Date Filters
# =============================
st.subheader("🗓️ Filter by Date Range")

col1, col2 = st.columns(2)
min_date = df["Posting Date"].min()
max_date = df["Posting Date"].max()

with col1:
    start_date = st.date_input("Start Date", min_date)

with col2:
    end_date = st.date_input("End Date", max_date)

mask = (df["Posting Date"] >= pd.to_datetime(start_date)) & (
    df["Posting Date"] <= pd.to_datetime(end_date)
)
filtered_df = df[mask].copy()

st.write(f"### Showing transactions from **{start_date} → {end_date}**")
st.write(f"Total transactions: **{len(filtered_df)}**")

# =========================================================
# 0️⃣ CLEAN COLUMNS
# =========================================================

# Remove time from Posting Date
filtered_df["Posting Date"] = filtered_df["Posting Date"].dt.date

# Format Amount (keep numeric + formatted version)
# FORMAT Amount + Balance (remove .00000 but keep them numeric underneath)
filtered_df["Amount"] = filtered_df["Amount"].astype(float).round(2)
filtered_df["Balance"] = filtered_df["Balance"].astype(float).round(2)

# For display only (avoid breaking charts or grouping)
filtered_df["Amount_str"] = filtered_df["Amount"].map("{:.2f}".format)
filtered_df["Balance_str"] = filtered_df["Balance"].map("{:.2f}".format)


# Positive value for spending bucket logic
filtered_df["SpendPos"] = filtered_df["Amount"].abs()

# =========================================================
# UNIFIED BUCKET COLUMN
# =========================================================

def bucketize(amount, detail):
    if detail == "CREDIT":
        return "Income"
    if amount < 10:
        return "Micro (<$10)"
    elif amount < 30:
        return "Small ($10–$30)"
    elif amount < 100:
        return "Medium ($30–$100)"
    elif amount < 300:
        return "Large ($100–$300)"
    else:
        return "Major (>$300)"

filtered_df["Bucket"] = filtered_df.apply(
    lambda row: bucketize(row["SpendPos"], row["Details"]), axis=1
)

# =============================
# 1️⃣ Spending Over Time Chart
# =============================
st.markdown("### 📈 Spending Over Time")

daily = (
    filtered_df.copy()
    .set_index(pd.to_datetime(filtered_df["Posting Date"]))
    .resample("D")["Amount"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily,
    x="Posting Date",
    y="Amount",
    title="Daily Spending Trend",
    markers=True,
)

fig.update_traces(line=dict(color="#4a74c9", width=3))
fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 2️⃣ WEEKDAY SPENDING HEATMAP
# =========================================================
st.subheader("📅 Weekly Spending Heatmap")

filtered_df["Weekday"] = pd.to_datetime(filtered_df["Posting Date"]).dt.day_name()


weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekday_summary = (
    filtered_df.groupby("Weekday")["SpendPos"]
    .sum()
    .reindex(weekday_order)
    .reset_index()
)

fig1 = px.imshow(
    [weekday_summary["SpendPos"]],
    labels=dict(x="Day of Week", color="Total Spend ($)"),
    x=weekday_summary["Weekday"],
    aspect="auto",
    color_continuous_scale="Blues",
)

fig1.update_layout(margin=dict(l=10, r=10, t=40, b=40))
st.plotly_chart(fig1, use_container_width=True)

st.write("### Weekday Summary")
st.dataframe(weekday_summary.rename(columns={"SpendPos": "Spending"}), hide_index=True)

# =========================================================
# 3️⃣ SPENDING BUCKETS (Only DEBIT spending, always positive)
# =========================================================

st.subheader("💵 Spending Buckets")

# Only debit = actual spending
spend_df = filtered_df[filtered_df["Details"] == "DEBIT"].copy()

# Always use positive values for spending calculations
spend_df["SpendPos"] = spend_df["Amount"].abs()

# Assign buckets again to avoid missing updates
spend_df["Bucket"] = spend_df["SpendPos"].apply(lambda x: bucketize(x, "DEBIT"))

# Group totals
bucket_summary = (
    spend_df.groupby("Bucket")["SpendPos"]
    .sum()
    .reset_index()
    .rename(columns={"SpendPos": "Total Spend"})
)

# Ensure correct order
bucket_order = [
    "Micro (<$10)",
    "Small ($10–$30)",
    "Medium ($30–$100)",
    "Large ($100–$300)",
    "Major (>$300)",
]

bucket_summary["Bucket"] = pd.Categorical(bucket_summary["Bucket"], bucket_order)
bucket_summary = bucket_summary.sort_values("Bucket")

# Better gradient blues
colors = ["#e2ecff", "#bcd4ff", "#8bb8ff", "#5e91ff", "#2f63ff"]

fig2 = px.bar(
    bucket_summary,
    x="Bucket",
    y="Total Spend",
    text_auto=".2s",
    title="Spending by Amount Bucket",
    color="Bucket",
    color_discrete_sequence=colors,
)

fig2.update_layout(
    xaxis_title="Bucket",
    yaxis_title="Total Spend ($)",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)
st.write("### Bucket Breakdown")
st.dataframe(bucket_summary, hide_index=True)

# =============================
# 4️⃣ Detailed Table (Bucket colored)
# =============================

st.markdown("### 🧾 Detailed Transactions")

num_rows = st.slider("Rows to display:", 5, 50, 15)

table_df = filtered_df[
    ["Details", "Posting Date", "Description", "Amount_str", "Balance_str", "Bucket"]
].rename(columns={
    "Amount_str": "Amount",
    "Balance_str": "Balance"
})

# ----- Color map for buckets -----
bucket_colors = {
    "Income": "#b3e6b3",
    "Micro (<$10)": "#e0ecff",
    "Small ($10–$30)": "#bfd6ff",
    "Medium ($30–$100)": "#9abfff",
    "Large ($100–$300)": "#6f9dff",
    "Major (>$300)": "#4666ff",
}

def highlight_row(row):
    color = bucket_colors.get(row["Bucket"], "#ffffff")
    return [f"background-color: {color}; color:black;"] * len(row)

styled_table = table_df.style.apply(highlight_row, axis=1)
st.dataframe(styled_table, hide_index=True)
