import streamlit as st
from sqlalchemy import text
from database import get_engine

# Page configuration
st.set_page_config(page_title="Set Budget Goals", page_icon="🎯")
st.title("🎯 Set Budget Goals")

# Session-based email retrieval
email = st.session_state.get("email", "")

if not email:
    st.warning("Please go to the Home page and enter your email before proceeding.")
else:
    income = st.number_input("Enter your monthly income ($)", min_value=0.0, step=100.0)

    st.write("Allocate your income using the 50/30/20 rule:")
    needs_percent = st.slider("Needs (%)", 0, 100, 50)
    wants_percent = st.slider("Wants (%)", 0, 100, 30)
    savings_percent = st.slider("Savings (%)", 0, 100, 20)

    total_percent = needs_percent + wants_percent + savings_percent

    if total_percent != 100:
        st.error("The total allocation must be exactly 100%.")
    elif income == 0:
        st.info("Please enter your income to continue.")
    else:
        if st.button("Save Budget Goals"):
            try:
                engine = get_engine()
                with engine.begin() as conn:
                    # Get user ID
                    user_result = conn.execute(
                        text("SELECT id FROM users WHERE email = :email"),
                        {"email": email}
                    ).fetchone()

                    if user_result:
                        user_id = user_result[0]
                        # Insert or update goals
                        conn.execute(text("""
                            INSERT INTO budget_goals (user_id, income, needs_percent, wants_percent, savings_percent)
                            VALUES (:user_id, :income, :needs, :wants, :savings)
                            ON CONFLICT (user_id)
                            DO UPDATE SET income = EXCLUDED.income,
                                          needs_percent = EXCLUDED.needs_percent,
                                          wants_percent = EXCLUDED.wants_percent,
                                          savings_percent = EXCLUDED.savings_percent
                        """), {
                            "user_id": user_id,
                            "income": income,
                            "needs": needs_percent,
                            "wants": wants_percent,
                            "savings": savings_percent
                        })
                        st.success("✅ Budget goals saved successfully!")
                    else:
                        st.error("❌ No user found with this email.")
            except Exception as e:
                st.error(f"❌ Failed to save budget goals: {e}")
