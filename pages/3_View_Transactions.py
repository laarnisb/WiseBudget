import streamlit as st
import pandas as pd
from database import get_transactions_by_user
from utils import get_current_user_email

st.set_page_config(page_title="📋 View Transactions", page_icon="📋")
st.title("📋 Your Transactions")

email = get_current_user_email()

if not email:
    st.warning("Please log in to view transactions.")
    st.stop()

transactions = get_transactions_by_user(email)

if transactions.empty:
    st.info("ℹ️ No transactions found.")
else:
    st.dataframe(transactions)
