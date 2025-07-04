import streamlit as st
from sqlalchemy import text
from database import get_engine
from datetime import datetime

st.set_page_config(page_title="Set Budget Goals", page_icon="🎯")
st.title("🎯 Set Budget Goals")

email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

income = st.number_input("Enter your monthly income ($)", min_value=0.0, format="%.2f")
needs = st.slider("Needs (%)", 0, 100, 50)
wants = st.slider("Wants (%)", 0, 100, 30)
savings = st.slider("Savings (%)", 0, 100, 20)

if needs + wants + savings != 100:
    st.error("🚫 The total percentage must equal 100%.")
else:
    if st.button("Save Budget Goals"):
        try:
            engine = get_engine()
            with engine.connect() as conn:
                user_query = text("SELECT id FROM users WHERE email = :email")
                user_result = conn.execute(user_query, {"email": email}).fetchone()

                if not user_result:
                    st.error("User not found. Please register first.")
                else:
                    user_id = user_result[0]
                    insert_query = text("""
                        INSERT INTO budget_goals (user_id, income, needs_percent, wants_percent, savings_percent, created_at)
                        VALUES (:user_id, :income, :needs, :wants, :savings, :created_at)
                        ON CONFLICT (user_id) DO UPDATE SET
                        income = EXCLUDED.income,
                        needs_percent = EXCLUDED.needs_percent,
                        wants_percent = EXCLUDED.wants_percent,
                        savings_percent = EXCLUDED.savings_percent,
                        created_at = EXCLUDED.created_at
                    """)
                    conn.execute(insert_query, {
                        "user_id": user_id,
                        "income": income,
                        "needs": needs,
                        "wants": wants,
                        "savings": savings,
                        "created_at": datetime.utcnow()
                    })
                    st.success("✅ Budget goals saved successfully!")

        except Exception as e:
            st.error(f"❌ Failed to save budget goals: {e}")
