import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_transactions

st.set_page_config(page_title="Budget Planner", layout="wide")
st.title("📝 Budget Planner")

# -------------------------
# Load Transaction Data
# -------------------------
df = load_transactions()

# Ensure Posting Date is datetime
df["Posting Date"] = pd.to_datetime(df["Posting Date"], errors="coerce")
df = df.dropna(subset=["Posting Date"])  # clean any broken rows

# Clean Amount Column
# Negative → expense → convert to positive
# Positive → income → ignore (0)
df["CleanAmount"] = df["Amount"].apply(lambda x: abs(x) if x < 0 else 0)

# Month column
df["Month"] = df["Posting Date"].dt.to_period("M").astype(str)

# -------------------------
# Select Month
# -------------------------
st.subheader("Select a month to plan:")

all_months = sorted(df["Month"].unique())
month = st.selectbox("", all_months)

# Filter for selected month
month_df = df[df["Month"] == month]

st.write(f"### Budget for **{month}**")

# -------------------------
# Categories + Session State
# -------------------------
categories = sorted(df["Category"].unique())

# Initialize session_state for budgets
if "budgets" not in st.session_state:
    st.session_state.budgets = {}

# Default = $300 per category
if month not in st.session_state.budgets:
    st.session_state.budgets[month] = {cat: 300 for cat in categories}

st.subheader("💵 Set Your Budgets")

# -------------------------
# Budget Inputs
# -------------------------
updated_budgets = {}

for cat in categories:
    current_budget = st.session_state.budgets[month].get(cat, 300)

    updated_value = st.number_input(
        f"{cat} Budget ($)",
        min_value=0.0,
        value=float(current_budget),
        step=10.0,
        key=f"{month}_{cat}_budget"
    )

    updated_budgets[cat] = float(updated_value)

# Save budgets
st.session_state.budgets[month] = updated_budgets

# -------------------------
# Spending Summary Table
# -------------------------
summary = (
    month_df.groupby("Category")["CleanAmount"]
    .sum()
    .reset_index()
    .rename(columns={"CleanAmount": "Spent"})
)

# Attach budgets
summary["Budget"] = summary["Category"].map(st.session_state.budgets[month])
summary["Budget"].fillna(0, inplace=True)

# Add categories with budgets but no spending
for cat, b in st.session_state.budgets[month].items():
    if cat not in summary["Category"].values:
        summary.loc[len(summary)] = [cat, 0, b]

# Status Logic
def status_logic(r):
    if r["Budget"] == 0:
        return "Good"
    pct = (r["Spent"] / r["Budget"]) * 100
    if pct > 100: return "Over"
    if pct > 80: return "Near"
    return "Good"

summary["Status"] = summary.apply(status_logic, axis=1)
summary = summary.sort_values("Category")

st.markdown("### 📋 Budget Overview")
st.dataframe(summary, hide_index=True)

# -------------------------
# Plot: Spending vs Budget
# -------------------------
st.subheader(f"📊 Spending vs Budget — {month}")

chart_df = summary.melt(
    id_vars="Category",
    value_vars=["Spent", "Budget"],
    var_name="Type",
    value_name="Amount"
)

color_map = {
    "Spent": "rgba(135, 206, 250, 0.85)",  # blue
    "Budget": "rgba(255, 255, 255, 0.35)"  # light white
}

fig = px.bar(
    chart_df,
    x="Category",
    y="Amount",
    color="Type",
    barmode="group",
    color_discrete_map=color_map,
    text_auto=".2s",
)

fig.update_layout(
    template="plotly_dark",
    title=f"Spending vs Budget — {month}",
    title_font=dict(size=26),
    xaxis_title="Category",
    yaxis_title="Amount ($)",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    bargap=0.30,
    legend_title=None,
)

fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")
fig.update_traces(width=0.45)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Monthly Summary
# -------------------------
total_budget = sum(st.session_state.budgets[month].values())
total_spent = month_df["CleanAmount"].sum()
remaining = total_budget - total_spent

st.subheader("📌 Monthly Summary")
st.write(f"**Total Budget:** ${total_budget:,.2f}")
st.write(f"**Total Spent:** ${total_spent:,.2f}")

if remaining > 0:
    st.success(f"🎉 You are **${remaining:,.2f} under budget** for {month}!")
else:
    st.error(f"⚠️ You are **${abs(remaining):,.2f} over budget** this month.")
