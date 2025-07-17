import streamlit as st
import pandas as pd
from utils import get_user_id_by_email
from database import fetch_budget_goals_by_user, get_transactions_by_user

st.set_page_config(page_title="Budget Recommendations", page_icon="💡")
st.title("💡 Personalized Budget Recommendations")

# Get logged-in user's email
if "email" not in st.session_state:
    st.warning("⚠️ Please log in to access budget recommendations.")
    st.stop()

email = st.session_state["email"]
user_id = get_user_id_by_email(email)

# Get budget goals
budget_goals = fetch_budget_goals_by_user(user_id)

# 🛑 Early exit if no goals
if not budget_goals:
    st.warning("No budget goals found. Please set your 50/30/20 budget first.")
    st.stop()

goals_df = pd.DataFrame(budget_goals)
goals_df.rename(columns={"category": "Category", "budget_amount": "Target"}, inplace=True)

# Get user transactions
transactions = get_transactions_by_user(user_id)
if not transactions:
    st.warning("No transactions found.")
    st.stop()

df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

latest_month = df["month"].max()
df_month = df[df["month"] == latest_month]

# Summarize spending
category_actuals = df_month.groupby("category")["amount"].sum().reset_index()
category_actuals.rename(columns={"category": "Category", "amount": "Actual"}, inplace=True)

# Merge with goals
summary = pd.merge(goals_df, category_actuals, on="Category", how="left").fillna(0)

# Normalize to percentages
total_spent = summary["Actual"].sum()
summary["Actual %"] = (summary["Actual"] / total_spent) * 100
summary["Target %"] = summary["Target"]
summary["Difference %"] = summary["Target %"] - summary["Actual %"]

# Format
summary["Target %"] = summary["Target %"].map("{:.2f}%".format)
summary["Actual %"] = summary["Actual %"].map("{:.2f}%".format)
summary["Difference %"] = summary["Difference %"].map("{:+.2f}%".format)

# Display
st.subheader("📊 Budget Allocation Summary")
st.dataframe(summary[["Category", "Target %", "Actual %", "Difference %"]], use_container_width=True)

# Recommendations
st.subheader("📋 Recommendations")
for _, row in summary.iterrows():
    category = row["Category"]
    diff_val = float(row["Difference %"].replace("%", ""))
    if diff_val < -5:
        st.error(f"You're overspending on **{category}** by {-diff_val:.2f}%. Consider cutting back.")
    elif diff_val > 5:
        st.success(f"Excellent! You're underspending on **{category}** by {diff_val:.2f}%.")
    else:
        st.info(f"You're on track with **{category}** spending.")
