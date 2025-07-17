import streamlit as st
import pandas as pd
from database import fetch_transactions_by_email, fetch_budget_goals

st.set_page_config(page_title="Budget Recommendations", page_icon="💡")
st.title("💡 Personalized Budget Recommendations")

email = st.session_state.get("email")
if not email:
    st.error("⚠️ Please log in to view this page.")
    st.stop()

# Fetch data
transactions = fetch_transactions_by_email(email)
budget_goals = fetch_budget_goals(email)

if transactions.empty:
    st.warning("No transactions found.")
    st.stop()

# Preprocess
transactions["date"] = pd.to_datetime(transactions["date"])
transactions["month"] = transactions["date"].dt.to_period("M").astype(str)
latest_month = transactions["month"].max()
monthly_data = transactions[transactions["month"] == latest_month]

monthly_income = monthly_data[monthly_data["category"] == "Income"]["amount"].sum()
monthly_data = monthly_data[monthly_data["category"] != "Income"]
category_actuals = monthly_data.groupby("category")["amount"].sum().abs().reset_index()
category_actuals.rename(columns={"amount": "Actual", "category": "Category"}, inplace=True)

# Process goals
goals_df = pd.DataFrame(budget_goals if isinstance(budget_goals, list) else [])
if not goals_df.empty:
    goals_df.rename(columns={"category": "Category"}, inplace=True)
    if "budget_amount" in goals_df.columns:
        goals_df["Target (%)"] = goals_df["budget_amount"]
    else:
        goals_df["Target (%)"] = 0
else:
    goals_df = pd.DataFrame(columns=["Category", "Target (%)"])

# Compute actual %
category_actuals["Actual (%)"] = (category_actuals["Actual"] / monthly_income * 100).round(2)
goals_df["Target (%)"] = goals_df["Target (%)"].round(2)

# Merge
summary = pd.merge(goals_df[["Category", "Target (%)"]], category_actuals[["Category", "Actual (%)"]], on="Category", how="left").fillna(0)
summary["Difference (%)"] = (summary["Target (%)"] - summary["Actual (%)"]).round(2)

# Display
st.subheader("📊 Budget Allocation Summary")
st.dataframe(summary.style.format({"Target (%)": "{:.2f}%", "Actual (%)": "{:.2f}%", "Difference (%)": "{:.2f}%"}), use_container_width=True)

# Recommendations
st.subheader("📝 Recommendations")
for _, row in summary.iterrows():
    diff = row["Difference (%)"]
    if diff < -5:
        st.error(f"❗ You are overspending on {row['Category']} by {abs(diff):.2f}% compared to your target.")
    elif diff > 5:
        st.success(f"✅ Excellent! You're spending less than your target on {row['Category']} by {diff:.2f}%.")
    else:
        st.info(f"ℹ️ Spending on {row['Category']} is on track.")
