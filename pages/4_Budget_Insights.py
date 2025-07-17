import streamlit as st
import pandas as pd
from database import get_transactions_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="💡 Budget Insights", page_icon="💡")
st.title("💡 Budget Insights")

# Get user email from session state
email = st.session_state.get("email")
if not email:
    st.warning("⚠️ Please log in to view budget insights.")
    st.stop()

# Get user ID
user_id = get_user_id_by_email(email)
if not user_id:
    st.error("User not found.")
    st.stop()

# Fetch transactions
transactions = get_transactions_by_user(user_id)
if not transactions:
    st.warning("No transactions found.")
    st.stop()

# Create DataFrame and preprocess
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df.dropna(subset=["date"], inplace=True)
df["month"] = df["date"].dt.to_period("M").astype(str)

# Month selection
available_months = sorted(df["month"].unique(), reverse=True)
if not available_months:
    st.warning("No transaction data available.")
    st.stop()

selected_month = st.selectbox("Select a month:", available_months)
df = df[df["month"] == selected_month]

# Monthly summary
monthly_summary = df.groupby("category")["amount"].sum().reset_index()
monthly_summary["amount"] = monthly_summary["amount"].round(2)

# Show table
st.subheader(f"Spending Summary for {selected_month}")
st.dataframe(monthly_summary, use_container_width=True)

# Pie chart (exclude Income)
pie_data = monthly_summary[monthly_summary["category"] != "Income"]
if not pie_data.empty:
    st.subheader("Spending Distribution (Pie Chart)")
    st.plotly_chart(
        {
            "data": [
                {
                    "type": "pie",
                    "labels": pie_data["category"],
                    "values": pie_data["amount"],
                    "hole": 0.3,
                }
            ],
            "layout": {"margin": {"t": 0, "b": 0}},
        },
        use_container_width=True,
    )
else:
    st.info("No spending data available for this month.")

# Bar chart (exclude Income)
bar_data = pie_data.copy()
if not bar_data.empty:
    st.subheader("Spending by Category (Bar Chart)")
    st.bar_chart(bar_data.set_index("category"))

# Budget Insight Message
top_category = pie_data.sort_values(by="amount", ascending=False).iloc[0]
st.success(
    f"💡 You spent the most on **{top_category['category']}** in {selected_month}, totaling ${top_category['amount']:.2f}."
)
