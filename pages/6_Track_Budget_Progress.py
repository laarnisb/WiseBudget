import streamlit as st
import pandas as pd
from database import fetch_transactions_by_email, fetch_budget_goals
import matplotlib.pyplot as plt

st.set_page_config(page_title="Track Budget Progress", page_icon="📊")
st.title("📊 Track Budget Progress")

# Get current user
email = st.session_state.get("email")
if not email:
    st.error("⚠️ Please log in to view this page.")
    st.stop()

# Select month
selected_month = st.selectbox("Select a month", options=sorted(set(pd.date_range(start="2025-01-01", periods=12, freq="M").strftime("%Y-%m"))))

# Fetch data
transactions = fetch_transactions_by_email(email)
budget_goals = fetch_budget_goals(email)

if transactions.empty:
    st.warning("No transactions found.")
    st.stop()

# Process data
transactions["date"] = pd.to_datetime(transactions["date"])
transactions["month"] = transactions["date"].dt.to_period("M").astype(str)

monthly_data = transactions[transactions["month"] == selected_month]
monthly_summary = monthly_data.groupby("category")["amount"].sum().reset_index()
monthly_income = monthly_summary.loc[monthly_summary["category"] == "Income", "amount"].sum()

# Convert to positive values for comparison
monthly_summary["amount"] = monthly_summary["amount"].abs()
monthly_summary = monthly_summary.rename(columns={"amount": "Actual", "category": "Category"})

# Budget Goals Processing
goals_df = pd.DataFrame(budget_goals if isinstance(budget_goals, list) else [])
if not goals_df.empty:
    goals_df.rename(columns={"category": "Category"}, inplace=True)
    if "budget_amount" in goals_df.columns:
        goals_df["Budgeted"] = goals_df["budget_amount"] / 100 * monthly_income
    else:
        goals_df["Budgeted"] = 0
else:
    goals_df = pd.DataFrame(columns=["Category", "Budgeted"])

# Merge
summary = pd.merge(goals_df[["Category", "Budgeted"]], monthly_summary, on="Category", how="outer").fillna(0)
summary["Difference"] = summary["Budgeted"] - summary["Actual"]
summary["Difference"] = summary["Difference"].round(2)
summary["Budgeted"] = summary["Budgeted"].round(2)
summary["Actual"] = summary["Actual"].round(2)

st.subheader(f"Summary for {selected_month}")
st.dataframe(summary.style.format({"Budgeted": "${:,.2f}", "Actual": "${:,.2f}", "Difference": "${:,.2f}"}), use_container_width=True)

# Bar chart with difference annotations
fig, ax = plt.subplots()
categories = summary["Category"]
x = range(len(categories))
ax.bar(x, summary["Budgeted"], width=0.4, label="Budgeted", align='center')
ax.bar([i + 0.4 for i in x], summary["Actual"], width=0.4, label="Actual", align='center')

# Add text labels
for i, diff in enumerate(summary["Difference"]):
    color = "green" if diff > 0 else "red"
    ax.text(i, max(summary["Budgeted"][i], summary["Actual"][i]) + 10, f"${diff:.2f}", ha="center", color=color)

ax.set_xticks([i + 0.2 for i in x])
ax.set_xticklabels(categories)
ax.set_ylabel("Amount ($)")
ax.set_title("Budgeted vs Actual Spending")
ax.legend()

st.pyplot(fig)

st.markdown("Use the sidebar to navigate through the app.")
