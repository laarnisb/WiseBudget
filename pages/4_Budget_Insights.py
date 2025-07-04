import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="Budget Insights", page_icon="📊")
st.title("📊 Budget Insights")

email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

engine = get_engine()

try:
    with engine.connect() as conn:
        query = text("SELECT amount, category FROM transactions WHERE user_email = :email")
        df = pd.read_sql(query, conn, params={"email": email})

    if df.empty:
        st.info("No transactions found.")
    else:
        # Group into Needs/Wants/Savings
        category_mapping = {
            "groceries": "Needs", "rent": "Needs", "utilities": "Needs", "transport": "Needs",
            "insurance": "Needs", "healthcare": "Needs", "internet": "Needs",
            "dining": "Wants", "entertainment": "Wants", "travel": "Wants", "shopping": "Wants",
            "subscriptions": "Wants", "savings": "Savings", "investment": "Savings",
            "emergency fund": "Savings", "retirement": "Savings"
        }
        df["group"] = df["category"].str.lower().map(category_mapping).fillna("Other")

        summary = df.groupby("group")["amount"].sum().reset_index()
        summary.columns = ["Category Group", "Total Spending"]

        st.subheader("Spending Summary")
        st.dataframe(summary)

        fig = px.pie(summary, names="Category Group", values="Total Spending", title="Spending by Category Group")
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error loading insights: {e}")
