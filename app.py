import streamlit as st
st.set_page_config(page_title="SpendWise", page_icon="💰", layout="wide")

from utils.data_cleaning import clean_data
from utils.loader import load_transactions

st.title("💰 SpendWise – Your Spending Assistant")

if "cleaned" not in st.session_state:
    st.session_state.cleaned = clean_data()

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
