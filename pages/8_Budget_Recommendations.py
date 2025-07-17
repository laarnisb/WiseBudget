import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import get_user_by_email, get_transactions_by_user, fetch_budget_goals_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="🧠 Budget Recommendations", page_icon="🧠")
st.title("🧠 Budget Recommendations")

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

    grouped = df.groupby("category")["amount"].sum().reset_index()
    grouped.columns = ["Category", "Actual ($)"]

    goal_data = {
        "Needs": budget_goals["income"] * (budget_goals["needs_percent"] / 100),
        "Wants": budget_goals["income"] * (budget_goals["wants_percent"] / 100),
        "Savings": budget_goals["income"] * (budget_goals["savings_percent"] / 100)
    }

    target_df = pd.DataFrame({
        "Category": ["Needs", "Wants", "Savings"],
        "Target ($)": [goal_data["Needs"], goal_data["Wants"], goal_data["Savings"]]
    })

    merged = pd.merge(target_df, grouped, on="Category", how="left").fillna(0)
    merged["Difference ($)"] = merged["Target ($)"] - merged["Actual ($)"]

    st.subheader("Target vs Actual Spending")
    st.dataframe(merged.style.format("{:.2f}"), use_container_width=True)

    # Recommendations
    st.subheader("💡 Recommendations")
    for _, row in merged.iterrows():
        category = row["Category"]
        diff = row["Difference ($)"]
        if diff < 0:
            st.markdown(f"🔴 You overspent on **{category}** by **${abs(diff):.2f}**. Consider reducing expenses.")
        elif diff > 0:
            st.markdown(f"🟢 You underspent on **{category}** by **${diff:.2f}**. Great job!")
        else:
            st.markdown(f"🟡 Your spending on **{category}** matched the target.")

    # Optional bar chart
    fig, ax = plt.subplots()
    merged.plot(
        x="Category", 
        y=["Target ($)", "Actual ($)"], 
        kind="bar", 
        ax=ax, 
        color=sns.color_palette("Set2")
    )
    ax.set_title("Spending Comparison")
    ax.set_ylabel("Amount ($)")
    ax.legend(title="Type")
    st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Failed to generate recommendations: {e}")
