import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="View Transactions", page_icon="📄")
st.title("📄 View Transactions")

email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

engine = get_engine()

try:
    with engine.connect() as conn:
        query = text("SELECT date, description, category, amount FROM transactions WHERE user_email = :email")
        df = pd.read_sql(query, conn, params={"email": email})

    if df.empty:
        st.info("No transactions found.")
    else:
        st.subheader("Your Transactions")
        st.dataframe(df)

except Exception as e:
    st.error(f"❌ Error retrieving transactions: {e}")
