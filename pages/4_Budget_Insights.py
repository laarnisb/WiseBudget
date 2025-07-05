import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="Budget Insights", layout="wide")
st.title("📊 Budget Insights")

# Ensure session-based email is available
if "email" not in st.session_state or not st.session_state.email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

email = st.session_state.email
engine = get_engine()

try:
    with engine.connect() as conn:
        query = text("""
            SELECT t.amount, t.category
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE u.email = :email
        """)
        result = conn.execute(query, {"email": email})
        data = pd.DataFrame(result.fetchall(), columns=result.keys())

    if data.empty:
        st.info("No transactions found for this user.")
    else:
        # Summarize spending by category
        summary = data.groupby("category")["amount"].sum().reset_index()
        summary.columns = ["Category", "Total Amount"]

        st.subheader("💡 Spending by Category")
        st.dataframe(summary)

        st.subheader("📊 Spending Breakdown")
        st.bar_chart(summary.set_index("Category"))

except Exception as e:
    st.error(f"❌ Error loading insights: {e}")
