import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_transactions_by_email

st.set_page_config(page_title="Track Budget Progress", page_icon="📈")
st.title("📈 Track Budget Progress")

if "email" not in st.session_state or not st.session_state.email:
    st.warning("⚠️ Please enter your email on the Home page.")
    st.stop()

# Fetch transactions from the database
df = get_transactions_by_email(st.session_state.email)

if df.empty:
    st.info("No transactions found. Please upload your data first.")
    st.stop()

# Map normalized categories to budget types
CATEGORY_TO_TYPE = {
    "Groceries": "Needs",
    "Rent": "Needs",
    "Utilities": "Needs",
    "Transport": "Needs",
    "Healthcare": "Needs",
    "Dining": "Wants",
    "Shopping": "Wants",
    "Entertainment": "Wants",
    "Travel": "Wants",
    "Savings": "Savings",
    "Investment": "Savings"
}
df["type"] = df["category"].map(CATEGORY_TO_TYPE).fillna("Other")

# Aggregate spending by type
summary = df.groupby("type")["amount"].sum().reset_index()

# Get target allocations
needs_pct = st.session_state.get("needs_pct", 50)
wants_pct = st.session_state.get("wants_pct", 30)
savings_pct = st.session_state.get("savings_pct", 20)

total_spent = summary["amount"].sum()
target_df = pd.DataFrame({
    "type": ["Needs", "Wants", "Savings"],
    "target": [
        total_spent * needs_pct / 100,
        total_spent * wants_pct / 100,
        total_spent * savings_pct / 100
    ]
})

# Merge actual vs. target
merged = pd.merge(summary, target_df, on="type", how="outer").fillna(0)

# Display table
st.subheader("💡 Budget Summary")
st.dataframe(merged.rename(columns={"amount": "Actual", "target": "Target"}), use_container_width=True)

# Plot
fig = px.bar(merged, x="type", y=["Actual", "Target"], barmode="group", title="Actual vs. Target Spending")
st.plotly_chart(fig, use_container_width=True)
