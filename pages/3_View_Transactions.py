import streamlit as st
import pandas as pd
from database import get_user_by_email, fetch_transactions_by_user

st.set_page_config(page_title="Your Transactions", page_icon="📄")
st.title("📄 Your Transactions")

# Get email from session state
if "email" not in st.session_state or not st.session_state["email"]:
    st.warning("⚠️ Please log in to view your transactions.")
    st.stop()

email = st.session_state["email"]
user = get_user_by_email(email)

if user:
    user_id = user["id"]
    transactions = fetch_transactions_by_user(user_id)
    
    if transactions:
        df = pd.DataFrame(transactions)
        df = df[["date", "description", "category", "amount"]]  # Display relevant columns
        df["date"] = pd.to_datetime(df["date"]).dt.date
        st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
    else:
        st.info("📭 No transactions found. Please upload your transactions.")
else:
    st.error("❌ User not found. Please register or log in again.")
