import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_transactions_by_user, get_user_by_email

st.set_page_config(page_title="📊 Budget Summary Reports", page_icon="📊")
st.title("📊 Budget Summary Reports")

# Get email from session
if "email" not in st.session_state:
    st.warning("⚠️ Please log in to view your budget summary.")
    st.stop()

email = st.session_state["email"]
user = get_user_by_email(email)
if not user:
    st.error("User not found.")
    st.stop()

user_id = user["id"]
transactions = get_transactions_by_user(user_id)

if not transactions:
    st.info("No transactions available for summary.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# Summarize by category and month
summary = df.groupby(["month", "category"])["amount"].sum().reset_index()

# Display Table
st.subheader("Summary Table")
st.dataframe(summary, use_container_width=True)

# Bar Chart
st.subheader("Monthly Spending by Category")
fig = px.bar(summary, x="month", y="amount", color="category", barmode="stack",
             labels={"month": "Month", "amount": "Amount Spent ($)", "category": "Category"},
             title="Spending Trends by Month")
st.plotly_chart(fig, use_container_width=True)
