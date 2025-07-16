import streamlit as st
import pandas as pd
from database import get_user_by_email, get_transactions_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="💡 Budget Recommendations", page_icon="💡")
st.title("💡 Budget Recommendations")

if "email" not in st.session_state or not st.session_state["email"]:
    st.warning("⚠️ Please log in to view recommendations.")
    st.stop()

email = st.session_state["email"]
user = get_user_by_email(email)
if not user:
    st.warning("User not found.")
    st.stop()

user_id = get_user_id_by_email(email)
transactions = get_transactions_by_user(user_id)

if not transactions:
    st.info("No transactions found.")
    st.stop()

df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

latest_month = df["month"].max()
latest_df = df[df["month"] == latest_month]

summary = latest_df.groupby("category")["amount"].sum().reset_index()
total_spent = summary["amount"].sum()

# Budget allocation rules
needs_budget = 0.50 * total_spent
wants_budget = 0.30 * total_spent
savings_budget = 0.20 * total_spent

# Mapping categories
category_map = {
    "Rent": "Needs",
    "Utilities": "Needs",
    "Groceries": "Needs",
    "Transportation": "Needs",
    "Healthcare": "Needs",
    "Dining": "Wants",
    "Entertainment": "Wants",
    "Shopping": "Wants",
    "Travel": "Wants",
    "Savings": "Savings",
    "Investments": "Savings",
    "Other": "Wants",
}

summary["Group"] = summary["category"].map(category_map).fillna("Wants")
grouped = summary.groupby("Group")["amount"].sum().reset_index()

# Display
st.subheader(f"Spending Recommendations for {latest_month}")
st.write("Based on the 50/30/20 rule:")

rec_table = pd.DataFrame({
    "Group": ["Needs", "Wants", "Savings"],
    "Budgeted": [needs_budget, wants_budget, savings_budget],
    "Actual": [
        grouped[grouped["Group"] == "Needs"]["amount"].sum(),
        grouped[grouped["Group"] == "Wants"]["amount"].sum(),
        grouped[grouped["Group"] == "Savings"]["amount"].sum(),
    ]
})
rec_table["Difference"] = rec_table["Actual"] - rec_table["Budgeted"]

st.dataframe(rec_table.style.format(precision=2), use_container_width=True)

# Insight message
for _, row in rec_table.iterrows():
    diff = row["Difference"]
    label = row["Group"]
    if diff > 0:
        st.warning(f"⚠️ You overspent on **{label}** by ${diff:.2f}.")
    elif diff < 0:
        st.success(f"✅ You are under your **{label}** budget by ${-diff:.2f}.")
