import streamlit as st
st.set_page_config(page_title="SpendWise", page_icon="💰", layout="wide")



st.title("💰 SpendWise – Your Spending Assistant")


df = load_transactions()

st.markdown("""
### Welcome to SpendWise  
Select a page from the sidebar to get started:

- 📝 Budget Planner
- 📊 Category Dashboard          
- 💭 Sentiment Analysis
- 💸 Spending Forecast   
- 🏪 Spending Insights  
""")
