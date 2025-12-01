import streamlit as st
from utils.loader import load_transactions
from agents.root import run_root_agent

st.title("💬 Ask SpendWise")

df = load_transactions()

if "history" not in st.session_state:
    st.session_state.history = []

question = st.chat_input("Ask something about your spending...")

if question:
    st.session_state.history.append(("user", question))

    with st.spinner("Thinking..."):
        analysis, advice = run_root_agent(question, df)

    st.session_state.history.append(("assistant", advice))

# Display chat
for role, content in st.session_state.history:
    if role == "user":
        with st.chat_message("user"):
            st.write(content)
    else:
        with st.chat_message("assistant"):
            st.write(content)
