import streamlit as st
from sqlalchemy import text
from database import get_connection, get_user_id

st.set_page_config(page_title="Set Budget Goals", page_icon="🎯")

st.title("🎯 Set Budget Goals")

st.markdown("Define your monthly income and allocate it according to the 50/30/20 rule or your custom preferences.")

# Session email
user_email = st.session_state.get("user_email", None)

if not user_email:
    st.warning("Please log in to set your budget goals.")
    st.stop()

# Get current user_id
user_id = get_user_id(user_email)
if not user_id:
    st.error("User not found in database.")
    st.stop()

# Sliders for income and goals
income = st.number_input("Enter your monthly income ($)", min_value=0.0, step=100.0)

needs_pct = st.slider("Needs (%)", min_value=0, max_value=100, value=50)
wants_pct = st.slider("Wants (%)", min_value=0, max_value=100, value=30)
savings_pct = st.slider("Savings (%)", min_value=0, max_value=100, value=20)

total_pct = needs_pct + wants_pct + savings_pct
if total_pct != 100:
    st.error("The total allocation must equal 100%.")
    st.stop()

# Submit
if st.button("Save Budget Goals"):
    with get_connection().begin() as conn:
        result = conn.execute(
            text("SELECT id FROM budget_goals WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchone()

        if result:
            conn.execute(
                text("""
                    UPDATE budget_goals
                    SET income = :income, needs_pct = :needs, wants_pct = :wants, savings_pct = :savings
                    WHERE user_id = :user_id
                """),
                {
                    "income": income,
                    "needs": needs_pct,
                    "wants": wants_pct,
                    "savings": savings_pct,
                    "user_id": user_id
                }
            )
        else:
            conn.execute(
                text("""
                    INSERT INTO budget_goals (user_id, income, needs_pct, wants_pct, savings_pct)
                    VALUES (:user_id, :income, :needs, :wants, :savings)
                """),
                {
                    "user_id": user_id,
                    "income": income,
                    "needs": needs_pct,
                    "wants": wants_pct,
                    "savings": savings_pct
                }
            )
    st.success("✅ Budget goals saved successfully!")
