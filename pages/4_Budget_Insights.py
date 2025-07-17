
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_user_id_by_email
from database import get_transactions_by_user

st.set_page_config(page_title="Budget Insights", page_icon="🔍")
st.title("🔍 Budget Insights")

email = st.session_state.get("email", "")
if not email:
    st.warning("⚠️ Please log in to view budget insights.")
    st.stop()

user_id = get_user_id_by_email(email)
if not user_id:
    st.error("User not found.")
    st.stop()

transactions = get_transactions_by_user(user_id)
if not transactions:
    st.info("No transactions found.")
    st.stop()

df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# Filter out 'Income' and keep only spending categories
df = df[df["category"] != "Income"]
df = df[df["category"].isin(["Needs", "Wants", "Savings", "Other"])]

if df.empty:
    st.info("No relevant spending data found.")
    st.stop()

selected_month = st.selectbox("Select a Month", sorted(df["month"].unique(), reverse=True))
monthly_df = df[df["month"] == selected_month]

# Group and summarize
summary = monthly_df.groupby("category")["amount"].sum().reset_index()
summary["amount"] = summary["amount"].round(2)

# Color-blind friendly palette (Set2)
color_palette = {
    "Needs": "#66c2a5",
    "Wants": "#fc8d62",
    "Savings": "#8da0cb",
    "Other": "#e78ac3"
}
summary["color"] = summary["category"].map(color_palette)

# Reorder categories: Needs, Wants, Savings, Other
ordered_categories = [cat for cat in ["Needs", "Wants", "Savings", "Other"] if cat in summary["category"].values]
summary = summary.set_index("category").loc[ordered_categories].reset_index()

# Table
st.subheader(f"Spending Summary for {selected_month}")
st.dataframe(summary[["category", "amount"]].rename(columns={"amount": "Amount ($)"}).reset_index(drop=True), use_container_width=True)

# Bar Chart
st.subheader("Spending by Category")
fig_bar, ax_bar = plt.subplots()
ax_bar.bar(summary["category"], summary["amount"], color=summary["color"])
ax_bar.set_ylabel("Amount ($)")
ax_bar.set_xlabel("Category")
ax_bar.set_title(f"Spending in {selected_month}")
st.pyplot(fig_bar)

# Pie Chart
st.subheader("Spending Distribution")
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(
    summary["amount"],
    labels=summary["category"],
    autopct="%1.2f%%",
    startangle=90,
    colors=summary["color"]
)
ax_pie.axis("equal")
st.pyplot(fig_pie)

# Insight
top_cat = summary.loc[summary["amount"].idxmax(), "category"]
st.info(f"Your highest spending in **{selected_month}** was on **{top_cat}**.")
