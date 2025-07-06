import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_transactions_by_email

st.set_page_config(page_title="Budget Summary Reports", page_icon="📊")
st.title("📊 Budget Summary Reports")

if "email" not in st.session_state or not st.session_state.email:
    st.warning("⚠️ Please enter your email on the Home page.")
    st.stop()

# Fetch user transactions
df = get_transactions_by_email(st.session_state.email)

if df.empty:
    st.info("No transactions available. Please upload your transactions first.")
    st.stop()

# Correct category-to-type mapping
CATEGORY_TO_TYPE = {
    "Groceries": "Needs",
    "Rent": "Needs",
    "Utilities": "Needs",
    "Transport": "Needs",
    "Healthcare": "Needs",
    "Dining": "Wants",
    "Shopping": "Wants",
    "Entertainment": "Wants",
    "Travel": "Wants",
    "Savings": "Savings",
    "Investment": "Savings"
}
df["type"] = df["category"].map(CATEGORY_TO_TYPE).fillna("Other")

# Summarize by type
type_summary = df.groupby("type")["amount"].sum().reset_index()

# Display table
st.subheader("💵 Spending Breakdown")
st.dataframe(type_summary, use_container_width=True)

# Pie chart
st.subheader("📌 Spending Distribution")
fig = px.pie(type_summary, values="amount", names="type", title="Spending by Budget Type")
st.plotly_chart(fig, use_container_width=True)
