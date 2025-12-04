import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
from utils.loader import load_transactions

st.set_page_config(page_title="Spending Forecast", layout="wide")
st.title("💸 Spending Forecast")

# =============================
# Load and Prepare Data
# =============================
df = load_transactions()
df["Posting Date"] = pd.to_datetime(df["Posting Date"])

# We only want to forecast spending, so we filter for DEBIT transactions
spend_df = df[df["Details"] == "DEBIT"].copy()
spend_df["Amount"] = spend_df["Amount"].abs()

# Prophet requires the columns to be named 'ds' (datestamp) and 'y' (value)
spend_df = spend_df.rename(columns={"Posting Date": "ds", "Amount": "y"})

# Aggregate spending per day
daily_spend = spend_df.groupby("ds")["y"].sum().reset_index()

st.info("This forecast is based on your historical DEBIT transactions (spending).")

# =============================
# Forecasting
# =============================
st.subheader("🔮 Forecast Future Spending")

# Let user choose forecast period
periods_input = st.slider(
    "Select forecast period (days):", min_value=30, max_value=365, value=90
)

if st.button("Generate Forecast"):
    if len(daily_spend) > 2:
        with st.spinner("Generating forecast..."):
            # Initialize and train the Prophet model
            m = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=True,
                changepoint_prior_scale=0.05,
            )
            m.fit(daily_spend)

            # Create a future dataframe for the specified period
            future = m.make_future_dataframe(periods=periods_input)

            # Make the forecast
            forecast = m.predict(future)

            # Display the forecast plot
            st.markdown(f"### Forecast Plot for the Next {periods_input} Days")
            fig1 = plot_plotly(m, forecast)
            fig1.update_layout(
                title=f"Spending Forecast for Next {periods_input} Days",
                xaxis_title="Date",
                yaxis_title="Predicted Spend",
                template="plotly_dark",
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Display forecast components
            st.markdown("### Forecast Components")
            fig2 = m.plot_components(forecast)
            st.pyplot(fig2)

            # Display the raw forecast data
            st.markdown("### Forecast Data")
            st.dataframe(
                forecast[
                    ["ds", "yhat", "yhat_lower", "yhat_upper"]
                ].tail(periods_input),
                hide_index=True,
            )
    else:
        st.warning(
            "Not enough data to generate a forecast. Please upload more transactions."
        )

st.markdown("---")
st.write("### Historical Daily Spending")
st.dataframe(daily_spend.sort_values("ds", ascending=False), hide_index=True)
