import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_transactions_by_email

st.set_page_config(page_title="Track Budget Progress", page_icon="📊")
st.title("📊 Track Your Budget Progress")

email = st.session_state.get("email", "")
if not email:
    st.warning("⚠️ Please enter your email on the Home page first.")
    st.stop()

df = get_transactions_by_email(email)

if df.empty:
    st.info("ℹ️ No transactions found.")
else:
    st.subheader("Summary by Category")
    category_totals = df.groupby("category")["amount"].sum()
    st.dataframe(category_totals.reset_index().rename(columns={"amount": "Total Amount"}))

    st.subheader("Bar Chart")
    fig, ax = plt.subplots()
    category_totals.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount")
    ax.set_xlabel("Category")
    ax.set_title("Spending by Category")
    st.pyplot(fig)
