import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_transactions_by_user, get_budget_goals_by_user
from utils import get_current_user_email

st.set_page_config(page_title="Track Budget Progress", page_icon="📊")
st.title("📊 Track Budget Progress")

email = get_current_user_email()

if not email:
    st.warning("Please log in to view your budget progress.")
    st.stop()

# Get actual transactions
transactions = get_transactions_by_user(email)
if transactions.empty:
    st.info("No transactions found. Please upload your transactions.")
    st.stop()

# Get budget goals
goals = get_budget_goals_by_user(email)
if goals.empty:
    st.info("No budget goals found. Please set your budget goals first.")
    st.stop()

# Aggregate actual spending by category
actual_totals = (
    transactions.groupby("category")["amount"]
    .sum()
    .reindex(["Needs", "Wants", "Savings"], fill_value=0)
    .reset_index()
    .rename(columns={"amount": "Actual"})
)

# Merge with targets
merged = actual_totals.copy()
merged["Target"] = [
    goals["needs"].values[0],
    goals["wants"].values[0],
    goals["savings"].values[0],
]
merged = merged.rename(columns={"category": "type"})

# Show data preview
st.subheader("Budget Comparison Table")
st.dataframe(merged)

# Safely plot chart
if not merged.empty and all(col in merged.columns for col in ["type", "Actual", "Target"]):
    fig = px.bar(
        merged,
        x="type",
        y=["Actual", "Target"],
        barmode="group",
        title="Actual vs. Target Spending",
        labels={"value": "Amount", "type": "Category"},
    )
    st.plotly_chart(fig)
else:
    st.warning("Cannot display chart. Check if required columns or values are missing.")
