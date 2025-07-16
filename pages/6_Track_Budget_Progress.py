import streamlit as st
import pandas as pd
from utils import get_user_id_by_email
from database import fetch_transactions_by_user, fetch_budget_goals_by_user

st.set_page_config(page_title="📊 Track Budget Progress", page_icon="📊")
st.title("📊 Track Budget Progress")

user_email = st.session_state.get("email")
if not user_email:
    st.warning("⚠️ Please log in first to view your budget progress.")
    st.stop()

# Get user ID
user_id = get_user_id_by_email(user_email)
if not user_id:
    st.error("User not found.")
    st.stop()

# Fetch transactions
transactions = fetch_transactions_by_user(user_id)
if not transactions:
    st.warning("No transactions found.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

# Let user select a month
months = df["month"].unique().tolist()
selected_month = st.selectbox("Select a month", sorted(months, reverse=True))

# Filter for selected month
monthly_df = df[df["month"] == selected_month]

# Exclude 'Income' category from tracking
monthly_df = monthly_df[monthly_df["category"] != "Income"]

# Group and summarize actual spending
category_totals = monthly_df.groupby("category")["amount"].sum().to_dict()

# Fetch budget goals
budget_goals = fetch_budget_goals_by_user(user_id)

if not budget_goals:
    st.warning("No budget goals found. Please set your 50/30/20 goals first.")
    st.stop()

try:
    needs_percent = float(budget_goals["needs_percent"])
    wants_percent = float(budget_goals["wants_percent"])
    savings_percent = float(budget_goals["savings_percent"])
    income = float(budget_goals["income"])
except (KeyError, TypeError, ValueError) as e:
    st.error(f"Invalid budget goal data: {e}")
    st.stop()

# Compute budget targets
budget_targets = {
    "Needs": income * needs_percent / 100,
    "Wants": income * wants_percent / 100,
    "Savings": income * savings_percent / 100
}

# Prepare summary
summary_data = []
for category, budget in budget_targets.items():
    actual = category_totals.get(category, 0.0)
    difference = actual - budget
    summary_data.append({
        "Category": category,
        "Budgeted": budget,
        "Actual": actual,
        "Difference": difference
    })

summary_df = pd.DataFrame(summary_data)

st.subheader(f"Summary for {selected_month}")
st.dataframe(summary_df.style.format({
    "Budgeted": "${:,.2f}",
    "Actual": "${:,.2f}",
    "Difference": "${:,.2f}"
}))

st.caption("Use the sidebar to navigate through the app.")
