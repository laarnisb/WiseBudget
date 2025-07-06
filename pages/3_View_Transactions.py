import streamlit as st
import pandas as pd
from database import get_transactions_by_user
from utils import get_current_user_email

st.set_page_config(page_title="View Transactions", page_icon="📄")
st.title("📄 View Transactions")

# Get email from session
email = get_current_user_email()

if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

# Fetch and display transactions
df = get_transactions_by_user(email)

if df.empty:
    st.info("ℹ️ No transactions found for this user.")
else:
    st.success(f"✅ {len(df)} transaction(s) found.")
    st.dataframe(df, use_container_width=True)
