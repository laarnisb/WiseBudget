import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_user_by_email, get_transactions_by_user, fetch_budget_goals_by_user
from utils import extract_month, get_user_id_by_email

st.set_page_config(page_title="Budget Recommendations", page_icon="💡")
st.title("💡 Budget Recommendation for Next Month")

# Get logged-in user email from session
if "email" not in st.session_state or not st.session_state["email"]:
    st.warning("⚠️ Please log in to view this page.")
    st.stop()

email = st.session_state["email"]
user = get_user_by_email(email)
if not user:
    st.error("User not found.")
    st.stop()

user_id = get_user_id_by_email(email)
transactions = get_transactions_by_user(user_id)
budget_goals = fetch_budget_goals_by_user(user_id)

if not transactions:
    st.info("No transactions found to generate recommendations.")
    st.stop()

# Convert to DataFrame and preprocess
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# Categorize and aggregate
df_summary = df.groupby(["month", "category"])["amount"].sum().reset_index()
monthly_summary = df_summary.pivot(index="month", columns="category", values="amount").fillna(0).reset_index()

# Get latest month for recommendation
latest_month = monthly_summary["month"].max()
latest_data = monthly_summary[monthly_summary["month"] == latest_month]

# Compute totals
total_income = latest_data["Income"].values[0] if "Income" in latest_data else 0
total_needs = latest_data["Needs"].values[0] if "Needs" in latest_data else 0
total_wants = latest_data["Wants"].values[0] if "Wants" in latest_data else 0
total_savings = latest_data["Savings"].values[0] if "Savings" in latest_data else 0
total_other = latest_data["Other"].values[0] if "Other" in latest_data else 0

# Build summary table
summary = {
    "Category": ["Needs", "Wants", "Savings", "Other"],
    "Target (%)": [
        budget_goals.get("needs_percent", 0),
        budget_goals.get("wants_percent", 0),
        budget_goals.get("savings_percent", 0),
        0  # No target for Other
    ],
    "Actual (%)": [
        round((total_needs / total_income) * 100, 2) if total_income else 0,
        round((total_wants / total_income) * 100, 2) if total_income else 0,
        round((total_savings / total_income) * 100, 2) if total_income else 0,
        round((total_other / total_income) * 100, 2) if total_income else 0,
    ]
}
summary["Difference (%)"] = [round(t - a, 2) for t, a in zip(summary["Target (%)"], summary["Actual (%)"])]

recommendations_df = pd.DataFrame(summary)

st.subheader(f"Spending Summary - {latest_month}")
st.dataframe(recommendations_df, use_container_width=True)

# Color-blind friendly palette
colors = list(plt.get_cmap("Set2").colors)

# Bar chart
st.subheader("📉 Budget Target vs Actual (%)")
fig_bar, ax_bar = plt.subplots()
bar_width = 0.35
index = range(len(recommendations_df))

ax_bar.bar(index, recommendations_df["Target (%)"], bar_width, label="Target", color=colors)
ax_bar.bar([i + bar_width for i in index], recommendations_df["Actual (%)"], bar_width, label="Actual", color=colors)

ax_bar.set_xlabel("Category")
ax_bar.set_ylabel("Percentage")
ax_bar.set_title(f"Budget Target vs Actual - {latest_month}")
ax_bar.set_xticks([i + bar_width / 2 for i in index])
ax_bar.set_xticklabels(recommendations_df["Category"])
ax_bar.legend()
st.pyplot(fig_bar)

# Pie chart
st.subheader("🥧 Actual Spending Breakdown")
pie_data = latest_data.drop(columns=["month"])
pie_data = pie_data.drop(columns=["Income"], errors="ignore")  # exclude income
category_totals = pie_data.sum(axis=1).values[0]

if category_totals > 0:
    fig_pie, ax_pie = plt.subplots()
    pie_labels = pie_data.columns.tolist()
    pie_values = pie_data.values[0]

    ax_pie.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax_pie.axis("equal")
    st.pyplot(fig_pie)
else:
    st.info("Not enough data to show pie chart.")

# Insight section
st.subheader("Recommendations")
for _, row in recommendations_df.iterrows():
    category = row["Category"]
    diff = row["Difference (%)"]
    if category == "Other":
        continue
    if diff < -5:
        st.error(f"🔻 You overspent on **{category}** by {abs(diff):.2f}%. Consider reducing it next month.")
    elif diff > 5:
        st.success(f"✅ You underspent on **{category}** by {diff:.2f}%. Great job staying under budget!")
    else:
        st.info(f"⚖️ You’re on track with **{category}** spending.")

st.markdown("---")
st.markdown("These recommendations are based on your most recent month's activity. Use them to guide your **next month's budget plan.** 💡")
