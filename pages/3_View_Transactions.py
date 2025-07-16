import streamlit as st
import pandas as pd
from database import get_transactions_by_user

st.set_page_config(page_title="View Transactions", page_icon="📄")
st.title("📄 Your Transactions")

# Require login
if "email" not in st.session_state or not st.session_state.email:
    st.warning("Please log in to view your transactions.")
    st.stop()

# Get transactions from DB
user_email = st.session_state.email
transactions = get_transactions_by_user(user_email)

if not transactions:
    st.info("No transactions found.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"]).dt.date

# Optional filters
with st.expander("🔍 Filter Transactions", expanded=False):
    date_range = st.date_input("Filter by date range", [])
    category_filter = st.multiselect("Filter by category", df["category"].unique())

    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    if category_filter:
        df = df[df["category"].isin(category_filter)]

# Display
st.dataframe(
    df[["date", "description", "category", "amount"]].sort_values("date", ascending=False),
    use_container_width=True,
)

# Optional: Download button
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", data=csv, file_name="your_transactions.csv", mime="text/csv")
