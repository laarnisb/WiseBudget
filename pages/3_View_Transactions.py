import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="View Transactions", page_icon="📄")
st.title("📄 View Transactions")

email = st.session_state.get("email", "")
if not email:
    st.warning("⚠️ Please enter your email on the Home page first.")
    st.stop()

try:
    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT t.date, t.description, t.category, t.amount
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE u.email = :email
            ORDER BY t.date DESC
        """)
        result = conn.execute(query, {"email": email})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

        if df.empty:
            st.info("ℹ️ No transactions found for this user.")
        else:
            st.success(f"✅ {len(df)} transaction(s) found.")
            st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"❌ Error retrieving transactions: {e}")
