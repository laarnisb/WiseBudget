import streamlit as st
from database import supabase, get_user_by_email
from utils import require_login
from datetime import datetime

st.set_page_config(page_title="Set Budget Goals", page_icon="🎯")
st.title("🎯 Set Your Budget Goals")

# Require user to be logged in
require_login()

# Get current user from session
email = st.session_state.get("email")
user = get_user_by_email(email)
user_id = user["id"] if user else None

# Display form if user is logged in
if user_id:
    with st.form("budget_form"):
        st.subheader("Enter Your Monthly Budget and Allocation")

        income = st.number_input("Monthly Income ($)", min_value=0.0, format="%.2f")
        needs_percent = st.slider("Needs (%)", 0, 100, 50)
        wants_percent = st.slider("Wants (%)", 0, 100, 30)
        savings_percent = st.slider("Savings (%)", 0, 100, 20)

        if needs_percent + wants_percent + savings_percent != 100:
            st.warning("⚠️ Total allocation must be exactly 100%.")

        submitted = st.form_submit_button("Save Budget Goals")

        if submitted and (needs_percent + wants_percent + savings_percent == 100):
            data = [
                {
                    "user_id": user_id,
                    "category": "Needs",
                    "budget_amount": round(income * (needs_percent / 100), 2),
                    "created_at": datetime.utcnow().isoformat(),
                },
                {
                    "user_id": user_id,
                    "category": "Wants",
                    "budget_amount": round(income * (wants_percent / 100), 2),
                    "created_at": datetime.utcnow().isoformat(),
                },
                {
                    "user_id": user_id,
                    "category": "Savings",
                    "budget_amount": round(income * (savings_percent / 100), 2),
                    "created_at": datetime.utcnow().isoformat(),
                },
            ]
            try:
                supabase.table("budget_goals").insert(data).execute()
                st.success("✅ Budget goals saved successfully!")
            except Exception as e:
                st.error(f"❌ Failed to save budget goals: {e}")
else:
    st.warning("⚠️ You must be logged in to set your budget goals.")
