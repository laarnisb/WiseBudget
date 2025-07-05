import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_engine

st.set_page_config(page_title="Budget Summary Reports", layout="wide")
st.title("📋 Budget Summary Reports")

# Check if email is available in session
email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

# Get database engine
engine = get_engine()

# Retrieve user_id from users table
with engine.connect() as conn:
    result = conn.execute(
        "SELECT id FROM users WHERE email = %(email)s", {"email": email}
    ).fetchone()

    if not result:
        st.error("User not found. Please register first.")
        st.stop()

    user_id = result[0]

    # Load transactions
    df = pd.read_sql(
        "SELECT category, amount FROM transactions WHERE user_id = %(user_id)s",
        conn,
        params={"user_id": user_id}
    )

# Validate data
if df.empty:
    st.warning("No transactions found for this user.")
    st.stop()

# Summary by category
summary = df.groupby("category")["amount"].sum().reset_index()

# Display table
st.subheader("🧾 Spending Summary by Category")
st.dataframe(summary, use_container_width=True)

# Pie Chart
st.subheader("📊 Spending Breakdown (Pie Chart)")
fig_pie = px.pie(summary, names="category", values="amount", title="Spending Distribution")
st.plotly_chart(fig_pie, use_container_width=True)

# Stacked Bar Chart (with one bar showing breakdown)
st.subheader("📊 Spending Breakdown (Bar Chart)")
fig_bar = px.bar(summary, x="category", y="amount", color="category", title="Category-wise Spending")
st.plotly_chart(fig_bar, use_container_width=True)
