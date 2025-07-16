import streamlit as st
from database import get_user_by_email, insert_budget_goals
from datetime import datetime

st.set_page_config(page_title="Set Budget Goals", page_icon="🎯")
st.title("🎯 Set Your Budget Goals")

# Ensure session email is available
if "email" not in st.session_state or not st.session_state["email"]:
    st.warning("⚠️ Please log in to set your budget goals.")
    st.stop()

email = st.session_state["email"]
user = get_user_by_email(email)

if not user:
    st.error("User not found. Please register or try again.")
    st.stop()

user_id = user["id"]

st.markdown("### Enter Your Budget Information")
income = st.number_input("Monthly Income ($)", min_value=0.0, format="%.2f")

st.markdown("### Set Your Budget Allocation (%)")
needs = st.slider("Needs (%)", min_value=0, max_value=100, value=50)
wants = st.slider("Wants (%)", min_value=0, max_value=100, value=30)
savings = st.slider("Savings (%)", min_value=0, max_value=100, value=20)

# Warn if total percent isn't 100%
total = needs + wants + savings
if total != 100:
    st.warning(f"Total allocation is {total}%. Consider adjusting to make it 100%.")

if st.button("💾 Save Budget Goals"):
    success = insert_budget_goals(user_id, income, needs, wants, savings)
    if success:
        st.success("✅ Budget goals saved successfully!")
    else:
        st.error("❌ Failed to save budget goals. Please try again.")
