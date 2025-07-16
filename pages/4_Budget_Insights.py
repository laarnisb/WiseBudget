import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_transactions_by_user

st.set_page_config(page_title="Budget Insights", page_icon="📊")
st.title("📊 Budget Insights")

# Require login
if "email" not in st.session_state or not st.session_state.email:
    st.warning("Please log in to view budget insights.")
    st.stop()

# Fetch transactions
user_email = st.session_state.email
transactions = get_transactions_by_user(user_email)

if not transactions:
    st.info("No transactions found.")
    st.stop()

# Create DataFrame
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"]).dt.date
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["category"] = df["category"].str.title()

# Exclude income transactions
df = df[df["category"] != "Income"]

# Group by category
category_summary = df.groupby("category")["amount"].sum()
category_summary = category_summary[category_summary > 0]  # pie chart needs positive values

# Display summary
st.subheader("💡 Spending Summary by Category")
st.dataframe(category_summary.reset_index(), use_container_width=True)

# Pie chart
if not category_summary.empty:
    fig1, ax1 = plt.subplots()
    ax1.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Bar chart
    st.subheader("📈 Spending Distribution")
    fig2, ax2 = plt.subplots()
    category_summary.plot(kind="bar", ax=ax2, color="skyblue")
    ax2.set_ylabel("Amount ($)")
    ax2.set_title("Spending per Category")
    st.pyplot(fig2)

    # Optional feedback
    top_category = category_summary.idxmax()
    top_spent = category_summary.max()
    st.success(f"✅ You spent the most on **{top_category}**, totaling **${top_spent:.2f}**.")
else:
    st.info("No positive spending data to display charts.")
