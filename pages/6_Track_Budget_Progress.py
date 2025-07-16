import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_user_by_email, get_transactions_by_user, fetch_budget_goals_by_user

st.set_page_config(page_title="📊 Track Budget Progress", page_icon="📊")
st.title("📊 Track Budget Progress")

# Retrieve user email from session
if "email" not in st.session_state:
    st.warning("⚠️ Please log in to track your budget progress.")
    st.stop()

user_email = st.session_state["email"]
user = get_user_by_email(user_email)

if user is None:
    st.error("User not found.")
    st.stop()

user_id = user["id"]

try:
    # Fetch transactions and budget goals
    transactions = get_transactions_by_user(user_id)
    goals = fetch_budget_goals_by_user(user_id)

    if not transactions:
        st.warning("No transactions found for this user.")
        st.stop()

    if not goals:
        st.warning("No budget goals set yet. Please set goals first.")
        st.stop()

    df = pd.DataFrame(transactions)
    df = df[df["category"] != "Income"]  # Exclude Income

    # Calculate totals
    category_totals = df.groupby("category")["amount"].sum()
    total_spent = category_totals.sum()

    # Prepare goals lookup
    goals_dict = {item["category"]: item["budget_amount"] for item in goals}

    # Prepare comparison table
    comparison_data = []
    for category, spent in category_totals.items():
        goal = goals_dict.get(category, 0)
        status = "✅ On Track" if spent <= goal else "⚠️ Over Budget"
        comparison_data.append({
            "Category": category,
            "Spent": spent,
            "Budget Goal": goal,
            "Status": status
        })

    comparison_df = pd.DataFrame(comparison_data)

    # Show comparison table
    st.subheader("📋 Budget Comparison")
    st.dataframe(comparison_df, use_container_width=True)

    # Plot
    st.subheader("📊 Budget Utilization by Category")
    fig, ax = plt.subplots()
    ax.bar(comparison_df["Category"], comparison_df["Spent"], label="Spent", alpha=0.7)
    ax.bar(comparison_df["Category"], comparison_df["Budget Goal"], label="Goal", alpha=0.7)
    ax.set_ylabel("Amount ($)")
    ax.set_title("Spending vs Budget Goals")
    ax.legend()
    st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Failed to track budget progress: {str(e)}")
