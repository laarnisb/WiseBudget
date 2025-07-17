import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from database import get_transactions_by_user, fetch_budget_goals_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="Track Budget Progress", page_icon="📊")

st.title("📊 Track Budget Progress")

# Get email from session
email = st.session_state.get("email")

if not email:
    st.warning("⚠️ Please log in to view this page.")
    st.stop()

# Get user_id
user_id = get_user_id_by_email(email)
if not user_id:
    st.error("❌ User not found. Please register or check your email.")
    st.stop()

# Fetch data
transactions = get_transactions_by_user(user_id)
budget_goals = fetch_budget_goals_by_user(user_id)

if not transactions:
    st.warning("No transactions found.")
    st.stop()

if not budget_goals:
    st.warning("No budget goals found.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

# Filter by most recent month
latest_month = df["month"].max()
monthly_df = df[df["month"] == latest_month]

# Actual spending by category
actual_summary = monthly_df.groupby("category")["amount"].sum().reset_index()
actual_summary.columns = ["category", "actual_amount"]

# Budgeted amounts
income = budget_goals.get("income", 0)
budgeted_summary = pd.DataFrame({
    "category": ["Needs", "Wants", "Savings"],
    "budgeted_amount": [
        income * budget_goals.get("needs_percent", 0) / 100,
        income * budget_goals.get("wants_percent", 0) / 100,
        income * budget_goals.get("savings_percent", 0) / 100,
    ]
})

# Merge
summary = pd.merge(budgeted_summary, actual_summary, how="left", on="category").fillna(0)

# Calculate difference (target - actual; negative if overspent)
summary["difference"] = summary["budgeted_amount"] - summary["actual_amount"]

# Show summary table
st.subheader(f"Summary for {latest_month}")
st.dataframe(summary.style.format({
    "budgeted_amount": "${:,.2f}",
    "actual_amount": "${:,.2f}",
    "difference": "${:,.2f}"
}))

# Bar chart: Budgeted vs Actual
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(
    x=summary["category"],
    y=summary["budgeted_amount"],
    name="Budgeted"
))
bar_fig.add_trace(go.Bar(
    x=summary["category"],
    y=summary["actual_amount"],
    name="Actual"
))
bar_fig.update_layout(
    barmode="group",
    title=f"Budgeted vs. Actual Spending for {latest_month}",
    xaxis_title="Category",
    yaxis_title="Amount ($)",
    legend_title="Type"
)
st.plotly_chart(bar_fig)