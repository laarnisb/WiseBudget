import streamlit as st
import pandas as pd
from database import get_user_by_email, fetch_transactions_by_user

st.set_page_config(page_title="💡 Budget Insights", page_icon="💡")
st.title("💡 Budget Insights")

# Check session for email
if "email" not in st.session_state or not st.session_state["email"]:
    st.warning("⚠️ Please log in to view budget insights.")
    st.stop()

email = st.session_state["email"]
user = get_user_by_email(email)

if user:
    user_id = user["id"]
    transactions = fetch_transactions_by_user(user_id)

    if transactions:
        df = pd.DataFrame(transactions)
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M").astype(str)

        # Group by category and month
        category_summary = df.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0)

        st.subheader("📊 Monthly Spending by Category")
        st.dataframe(category_summary, use_container_width=True)

        st.bar_chart(category_summary)
    else:
        st.info("📭 No transactions found to analyze. Please upload your transactions.")
else:
    st.error("❌ User not found. Please log in again.")
