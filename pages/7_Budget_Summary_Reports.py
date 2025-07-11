import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_transactions_by_user
from utils import get_current_user_email

st.set_page_config(page_title="Budget Summary Reports", page_icon="📈")
st.title("📈 Budget Summary Reports")

# Get the user's email from session
email = get_current_user_email()

if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

# Fetch transactions
transactions = get_transactions_by_user(email)

if transactions.empty:
    st.info("ℹ️ No transactions found to generate a report.")
    st.stop()

# Normalize and group data
transactions["category"] = transactions["category"].str.title()
category_totals = transactions.groupby("category")["amount"].sum().reset_index()

# Display table
st.subheader("📊 Spending Breakdown by Category")
st.dataframe(category_totals)

# Plot pie chart
fig = px.pie(category_totals, names="category", values="amount", title="Spending Distribution")
st.plotly_chart(fig)

# Optional: stacked bar chart for time-based trends
transactions["date"] = pd.to_datetime(transactions["date"])
transactions["month"] = transactions["date"].dt.to_period("M").astype(str)
monthly_totals = transactions.groupby(["month", "category"])["amount"].sum().reset_index()

st.subheader("📆 Monthly Spending by Category")
fig2 = px.bar(
    monthly_totals,
    x="month",
    y="amount",
    color="category",
    title="Monthly Spending Trends",
    labels={"amount": "Amount ($)", "month": "Month"},
)
st.plotly_chart(fig2)
