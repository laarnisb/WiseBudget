import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import fetch_transactions_by_user

st.set_page_config(page_title="Budget Insights", page_icon="💡")
st.title("💡 Budget Insights")

# Ensure email is in session
if "email" not in st.session_state:
    st.warning("⚠️ Please log in to view budget insights.")
    st.stop()

email = st.session_state.email
transactions = fetch_transactions_by_user(email)

if not transactions:
    st.info("No transactions found.")
    st.stop()

df = pd.DataFrame(transactions)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Extract month
df["month"] = df["date"].dt.to_period("M")

# Exclude "Income" from category summaries
filtered_df = df[df["category"] != "Income"]

# Monthly spending summary
monthly_summary = filtered_df.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0).reset_index()

st.subheader("📊 Monthly Spending by Category")
st.dataframe(monthly_summary)

# Plot stacked bar chart
fig, ax = plt.subplots()
categories = monthly_summary.columns[1:]
bottom = None
for cat in categories:
    ax.bar(monthly_summary["month"].astype(str), monthly_summary[cat], bottom=bottom, label=cat)
    if bottom is None:
        bottom = monthly_summary[cat].copy()
    else:
        bottom += monthly_summary[cat]

ax.set_ylabel("Amount")
ax.set_title("Monthly Spending Distribution")
ax.legend()
st.pyplot(fig)
