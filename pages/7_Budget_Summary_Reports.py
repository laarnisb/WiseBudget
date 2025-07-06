import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_transactions_by_email

st.set_page_config(page_title="Budget Summary Reports", page_icon="📑")
st.title("📑 Budget Summary Reports")

email = st.session_state.get("email", "")
if not email:
    st.warning("⚠️ Please enter your email on the Home page first.")
    st.stop()

df = get_transactions_by_email(email)

if df.empty:
    st.info("ℹ️ No transactions found.")
else:
    st.subheader("Spending by Category")
    category_totals = df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots()
    ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    st.markdown("**Detailed Breakdown**")
    st.dataframe(category_totals.reset_index().rename(columns={"amount": "Total Amount"}))
