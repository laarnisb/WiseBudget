import streamlit as st
import pandas as pd
from database import get_transactions_by_user
from utils import extract_month, get_user_id_by_email

st.set_page_config(page_title="Budget Recommendations", page_icon="💡")
st.title("💡 Budget Recommendations")

if "email" not in st.session_state:
    st.warning("⚠️ Please log in to view recommendations.")
    st.stop()

email = st.session_state["email"]
user_id = get_user_id_by_email(email)

transactions = get_transactions_by_user(user_id)
if not transactions:
    st.info("No transactions found. Please upload your data.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(transactions)

# Ensure proper dtypes
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df.dropna(subset=["amount", "date", "category"], inplace=True)

# Extract latest month with data
df["month"] = df["date"].dt.to_period("M")
latest_month = df["month"].max()
current_month_df = df[df["month"] == latest_month]

if current_month_df.empty:
    st.info(f"No transactions found for {latest_month}.")
    st.stop()

# Compute total spending and actual percentages
total_spending = current_month_df["amount"].sum()
actual_percent = (
    current_month_df.groupby("category")["amount"].sum() / total_spending * 100
).reset_index()
actual_percent.columns = ["Category", "Actual (%)"]

# Define targets (exclude "Other")
target_percent = pd.DataFrame({
    "Category": ["Needs", "Wants", "Savings"],
    "Target (%)": [50, 30, 20]
})

# Merge target and actual
summary = pd.merge(target_percent, actual_percent, on="Category", how="left")
summary["Actual (%)"] = summary["Actual (%)"].fillna(0).round(2)
summary["Difference (%)"] = (summary["Target (%)"] - summary["Actual (%)"]).round(2)

# Display summary table
st.subheader(f"📅 Spending Summary for {latest_month}")
st.dataframe(summary, use_container_width=True)

# Generate recommendations
st.subheader("📌 Recommendations")

for _, row in summary.iterrows():
    category = row["Category"]
    diff = row["Difference (%)"]

    if diff > 5:
        st.info(f"💡 Consider increasing your **{category}** spending by {diff:.1f}% to meet your target.")
    elif diff < -5:
        st.warning(f"⚠️ You are overspending on **{category}** by {-diff:.1f}%. Try cutting back.")
    else:
        st.success(f"✅ Great job! Your **{category}** spending is on track.")
