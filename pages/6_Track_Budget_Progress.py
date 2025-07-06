# pages/6_Track_Budget_Progress.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_budget_goals, get_actual_spending_by_category
from auth import get_logged_in_user_email

st.set_page_config(page_title="Track Budget Progress", page_icon="📊")
st.title("📊 Track Budget Progress")

st.subheader("📉 Budget vs. Actual Spending")

# Get user email
user_email = get_logged_in_user_email()

if user_email:
    # Fetch data from the database
    budget_goals = get_budget_goals(user_email)
    actual_spending = get_actual_spending_by_category(user_email)

    # Define all categories
    categories = ["Needs", "Wants", "Savings", "Other"]

    # Create budgeted dictionary from fetched goals
    budgeted = {cat: 0 for cat in categories}
    for entry in budget_goals:
        category, amount = entry
        if category in budgeted:
            budgeted[category] = amount

    # Create actual spending dictionary from fetched data
    actual = {cat: 0 for cat in categories}
    for entry in actual_spending:
        category, total = entry
        if category in actual:
            actual[category] = total

    # Create DataFrame
    category_totals = pd.DataFrame({
        "Budgeted": budgeted,
        "Actual": actual
    }).T

    # Ensure numeric values and handle missing data
    category_totals = category_totals.fillna(0)
    category_totals = category_totals.astype(float)
    category_totals.loc["Difference"] = category_totals.loc["Actual"] - category_totals.loc["Budgeted"]

    # Display table
    st.dataframe(category_totals.T.style.format("{:.2f}"))

    # Bar chart
    st.subheader("📊 Bar Chart")
    fig, ax = plt.subplots()
    category_totals.T[["Budgeted", "Actual"]].plot(kind="bar", ax=ax)
    plt.ylabel("Amount ($)")
    plt.title("Budgeted vs. Actual Spending")
    st.pyplot(fig)

else:
    st.warning("⚠️ Please log in to view your budget progress.")
