import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import get_user_by_email, get_transactions_by_user, fetch_budget_goals_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="Track Budget Progress", page_icon="📊")
st.title("📊 Track Budget Progress")

if "email" not in st.session_state:
    st.warning("⚠️ Please log in to view this page.")
    st.stop()

email = st.session_state["email"]
user_id = get_user_id_by_email(email)

try:
    transactions = get_transactions_by_user(user_id)
    budget_goals = fetch_budget_goals_by_user(user_id)

    if not transactions or not budget_goals:
        st.warning("Please make sure both transactions and budget goals are available.")
        st.stop()

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)

    # Extract and filter by latest month
    df["month"] = df["date"].dt.to_period("M")
    latest_month = df["month"].max()
    df = df[df["month"] == latest_month]

    grouped = df.groupby("category")["amount"].sum().reset_index()

    budget_data = {
        "Needs": budget_goals["income"] * (budget_goals["needs_percent"] / 100),
        "Wants": budget_goals["income"] * (budget_goals["wants_percent"] / 100),
        "Savings": budget_goals["income"] * (budget_goals["savings_percent"] / 100)
    }

    actual_data = {
        cat: grouped[grouped["category"] == cat]["amount"].values[0] if cat in grouped["category"].values else 0
        for cat in ["Needs", "Wants", "Savings"]
    }

    summary = pd.DataFrame({
        "Category": ["Needs", "Wants", "Savings"],
        "Budgeted": [budget_data["Needs"], budget_data["Wants"], budget_data["Savings"]],
        "Actual": [actual_data["Needs"], actual_data["Wants"], actual_data["Savings"]]
    })
    summary["Difference"] = summary["Budgeted"] - summary["Actual"]

    # Show which month we're reporting
    st.subheader(f"Budget Progress for {latest_month}")

    st.dataframe(summary.style.format({"Budgeted": "{:.2f}", "Actual": "{:.2f}", "Difference": "{:.2f}"}), use_container_width=True)

    # Bar chart using Set2 palette
    fig, ax = plt.subplots()
    summary.plot(
        x="Category", 
        y=["Budgeted", "Actual"], 
        kind="bar", 
        ax=ax, 
        color=sns.color_palette("Set2")
    )
    ax.set_ylabel("Amount ($)")
    ax.set_title("Budgeted vs Actual Spending")
    ax.legend(title="Type")
    st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Failed to track budget progress: {e}")
