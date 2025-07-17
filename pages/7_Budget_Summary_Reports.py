import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_transactions_by_user
from utils import get_user_id_by_email
from collections import defaultdict

st.set_page_config(page_title="Budget Summary Reports", page_icon="📋")
st.title("📋 Budget Summary Reports")

# Colorblind-friendly palette
color_palette = {
    "Needs": "#66c2a5",
    "Wants": "#fc8d62",
    "Savings": "#8da0cb",
    "Other": "#e78ac3"
}

# Ensure user is logged in
if "email" not in st.session_state:
    st.warning("⚠️ Please log in to view your budget summary reports.")
    st.stop()

# Get transactions from Supabase
user_id = get_user_id_by_email(st.session_state["email"])
transactions = get_transactions_by_user(user_id)

if not transactions:
    st.info("No transactions found.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# Group and summarize
summary = df.groupby(["month", "category"])["amount"].sum().reset_index()
monthly_totals = summary.groupby("month")["amount"].sum().reset_index(name="total")

# Merge and compute percentages
summary = summary.merge(monthly_totals, on="month")
summary["percent"] = (summary["amount"] / summary["total"]) * 100

# Display latest month summary
latest_month = summary["month"].max()
latest_summary = summary[summary["month"] == latest_month].sort_values(by="percent", ascending=False)

st.subheader(f"Spending Summary for {latest_month}")
st.dataframe(latest_summary[["category", "amount", "percent"]].round(2), use_container_width=True)

# Prepare data for stacked bar chart
exclude_categories = ["Income"]
melted = df[~df["category"].isin(exclude_categories)]
monthly_summary = melted.groupby(["month", "category"])["amount"].sum().unstack().fillna(0)

# Reorder columns to match palette
ordered_categories = ["Needs", "Wants", "Savings", "Other"]
existing_categories = [cat for cat in ordered_categories if cat in monthly_summary.columns]
colors = [color_palette.get(cat, "#999999") for cat in existing_categories]

# Plot chart
fig, ax = plt.subplots()
monthly_summary[existing_categories].plot(kind="bar", stacked=True, ax=ax, color=colors)
ax.set_title("Monthly Spending by Category (excluding Income)")
ax.set_xlabel("Month")
ax.set_ylabel("Amount ($)")
st.pyplot(fig)
