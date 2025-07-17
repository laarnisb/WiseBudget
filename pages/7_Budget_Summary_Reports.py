import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_user_by_email, get_transactions_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="📋 Budget Summary Reports", page_icon="📋")
st.title("📋 Budget Summary Reports")

# Use the email from session state
if "email" not in st.session_state or not st.session_state["email"]:
    st.warning("⚠️ Please log in to view your budget summary.")
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

# Convert to DataFrame
df = pd.DataFrame(transactions)

# Ensure date column is in datetime format
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# Group and pivot
monthly_summary = (
    df.groupby(["month", "category"])["amount"]
    .sum()
    .reset_index()
    .pivot(index="month", columns="category", values="amount")
    .fillna(0)
    .reset_index()
)

# Display the summary table
st.dataframe(monthly_summary.style.format(precision=2), use_container_width=True)

# Download CSV
csv = monthly_summary.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Budget Summary CSV",
    data=csv,
    file_name="budget_summary.csv",
    mime="text/csv",
)

# Stacked bar chart (excluding Income)
exclude_categories = ["Income"]
melted = monthly_summary.melt(id_vars="month", var_name="category", value_name="amount")
filtered = melted[~melted["category"].isin(exclude_categories)]

fig, ax = plt.subplots()
filtered.pivot(index="month", columns="category", values="amount").plot(
    kind="bar", stacked=True, ax=ax
)
ax.set_title("Monthly Spending by Category (excluding Income)")
ax.set_xlabel("Month")
ax.set_ylabel("Amount ($)")
st.pyplot(fig)
