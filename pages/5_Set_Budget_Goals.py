import streamlit as st
from database import get_user_by_email, insert_budget_goal, get_budget_goals_by_user
from utils import require_login

st.set_page_config(page_title="Set Budget Goals", page_icon="🎯")
st.title("🎯 Set Your Budget Goals")

user_email = require_login()

if user_email:
    user = get_user_by_email(user_email)

    if user:
        income = st.number_input("Enter your monthly income ($)", min_value=0.0, format="%.2f")

        st.markdown("**Allocate percentages of your income to each category:**")
        needs_percent = st.slider("Needs (%)", min_value=0, max_value=100, value=50)
        wants_percent = st.slider("Wants (%)", min_value=0, max_value=100, value=30)
        savings_percent = st.slider("Savings (%)", min_value=0, max_value=100, value=20)

        total_percent = needs_percent + wants_percent + savings_percent
        if total_percent != 100:
            st.error("The total allocation must equal 100%. Please adjust the sliders.")
        else:
            if st.button("Save Budget Goals"):
                success = insert_budget_goal(user["id"], income, needs_percent, wants_percent, savings_percent)
                if success:
                    st.success("✅ Budget goals saved successfully!")
                else:
                    st.error("❌ Failed to save budget goals.")

        # Display existing goals
        st.markdown("---")
        st.subheader("📊 Your Budget Goals History")
        goals = get_budget_goals_by_user(user["id"])
        if goals:
            st.dataframe(goals)
        else:
            st.info("You haven't set any budget goals yet.")
