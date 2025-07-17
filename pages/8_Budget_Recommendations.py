import streamlit as st
import pandas as pd
from database import get_transactions_by_user, fetch_budget_goals_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="💡 Budget Recommendations", page_icon="💡")
st.title("💡 Budget Recommendations")

# Get user email
email = st.session_state.get("email")

if not email:
    st.warning("⚠️ Please log in to view this page.")
    st.stop()

# Get user_id
user_id = get_user_id_by_email(email)
if not user_id:
    st.error("❌ User not found.")
    st.stop()

# Fetch data
transactions = get_transactions_by_user(user_id)
budget_goals = fetch_budget_goals_by_user(user_id)

if not transactions or not budget_goals:
    st.warning("Missing transactions or budget goals.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

# Most recent month
latest_month = df["month"].max()
df = df[df["month"] == latest_month]

# Actual totals
actual_summary = df.groupby("category")["amount"].sum().reset_index()

# Calculate actual percentages
total_spent = actual_summary["amount"].sum()
actual_summary["actual_percent"] = (actual_summary["amount"] / total_spent * 100).round(2)

# Budget goals
income = budget_goals.get("income", 0)
goals_df = pd.DataFrame({
    "category": ["Needs", "Wants", "Savings"],
    "target_percent": [
        budget_goals.get("needs_percent", 0),
        budget_goals.get("wants_percent", 0),
        budget_goals.get("savings_percent", 0),
    ]
})

# Merge summaries
merged = pd.merge(goals_df, actual_summary, how="left", on="category").fillna(0)
merged["difference"] = (merged["target_percent"] - merged["actual_percent"]).round(2)

# Display summary table
st.subheader(f"Spending Performance for {latest_month}")
st.dataframe(merged[["category", "target_percent", "actual_percent", "difference"]].style.format({
    "target_percent": "{:.2f}%",
    "actual_percent": "{:.2f}%",
    "difference": "{:.2f}%"
}))

# Generate recommendations
st.subheader("Recommendations")
for _, row in merged.iterrows():
    category = row["category"]
    diff = row["difference"]

    if diff < -5:
        st.error(f"⚠️ You overspent on **{category}** by {abs(diff):.2f}%. Try cutting back next month.")
    elif diff > 5:
        st.success(f"✅ Great job! You spent {abs(diff):.2f}% less than your target for **{category}**.")
    else:
        st.info(f"📊 Your **{category}** spending is on track (within ±5%).")

st.info("Use the sidebar to navigate through the app.")
