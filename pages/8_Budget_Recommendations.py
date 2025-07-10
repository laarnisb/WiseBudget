import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine
from utils import get_current_user_email

st.set_page_config(page_title="Budget Recommendations", page_icon="💡")
st.title("💡 Personalized Budget Recommendations")

email = get_current_user_email()

if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

engine = get_engine()
with engine.connect() as conn:
    # Get user_id
    user_query = text("SELECT id FROM users WHERE email = :email")
    user_result = conn.execute(user_query, {"email": email}).fetchone()

    if not user_result:
        st.error("❌ User not found.")
        st.stop()

    user_id = user_result[0]

    # Fetch latest budget goals
    goals_query = text("""
        SELECT income, needs_percent, wants_percent, savings_percent
        FROM budget_goals
        WHERE user_id = :user_id
        ORDER BY created_at DESC
        LIMIT 1
    """)
    goals_result = conn.execute(goals_query, {"user_id": user_id}).fetchone()

    if not goals_result:
        st.warning("⚠️ No budget goals found. Please set your goals first.")
        st.stop()

    income, needs_pct, wants_pct, savings_pct = goals_result
    budget_targets = {
        "Needs": round(income * needs_pct / 100, 2),
        "Wants": round(income * wants_pct / 100, 2),
        "Savings": round(income * savings_pct / 100, 2)
    }

    # Fetch transaction data
    txn_query = text("""
        SELECT category, amount
        FROM transactions
        WHERE user_id = :user_id
    """)
    txn_df = pd.DataFrame(conn.execute(txn_query, {"user_id": user_id}).fetchall(),
                          columns=["category", "amount"])

if txn_df.empty:
    st.info("ℹ️ No transactions found for this user.")
    st.stop()

# Classify spending into groups
category_mapping = {
    "groceries": "Needs", "rent": "Needs", "utilities": "Needs", "transport": "Needs",
    "insurance": "Needs", "healthcare": "Needs", "internet": "Needs",
    "dining": "Wants", "entertainment": "Wants", "travel": "Wants", "shopping": "Wants",
    "subscriptions": "Wants",
    "savings": "Savings", "investment": "Savings", "emergency fund": "Savings", "retirement": "Savings"
}
txn_df["group"] = txn_df["category"].str.lower().map(category_mapping).fillna("Other")

actual_spending = txn_df.groupby("group")["amount"].sum().to_dict()
for group in ["Needs", "Wants", "Savings"]:
    actual_spending.setdefault(group, 0)

# Recommendation logic
st.subheader("📝 Recommendations")
for group in ["Needs", "Wants", "Savings"]:
    actual = actual_spending[group]
    target = budget_targets[group]
    variance = actual - target
    percent_diff = (variance / target) * 100 if target != 0 else 0

    if group == "Wants" and percent_diff > 10:
        st.warning(f"🔸 You're spending {percent_diff:.1f}% more on *{group}* than your target. Consider cutting back on non-essentials.")
    elif group == "Savings" and actual < target:
        shortfall = target - actual
        st.error(f"💰 You're behind on your *{group}* goal by ${shortfall:.2f}. Try automating transfers or adjusting spending in Wants.")
    elif group == "Needs" and actual < target * 0.9:
        st.success(f"✅ Great job! You're keeping your *{group}* expenses below target.")
    else:
        st.info(f"🧾 Your *{group}* spending is within acceptable range.")

# Show summary
st.subheader("📊 Summary")
summary_df = pd.DataFrame({
    "Target": pd.Series(budget_targets),
    "Actual": pd.Series(actual_spending)
})
summary_df["Variance"] = summary_df["Actual"] - summary_df["Target"]
summary_df["% Difference"] = (summary_df["Variance"] / summary_df["Target"] * 100).round(1)
st.dataframe(summary_df)
