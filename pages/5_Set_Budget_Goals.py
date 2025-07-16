import streamlit as st
from database import get_user_by_email, save_budget_goals

st.set_page_config(page_title="Set Budget Goals", page_icon="🎯")
st.title("🎯 Set Your Budget Goals")

if "email" not in st.session_state:
    st.warning("⚠️ Please log in to set your budget goals.")
else:
    user_email = st.session_state["email"]
    user = get_user_by_email(user_email)
    
    if user:
        user_id = user["id"]
        
        st.subheader("Enter Your Income")
        income = st.number_input("Monthly Income", min_value=0.0, step=100.0, format="%.2f")

        st.subheader("Set Budget Percentages")
        needs_percent = st.slider("Needs (%)", min_value=0, max_value=100, value=50)
        wants_percent = st.slider("Wants (%)", min_value=0, max_value=100, value=30)
        savings_percent = st.slider("Savings (%)", min_value=0, max_value=100, value=20)

        if needs_percent + wants_percent + savings_percent != 100:
            st.error("The percentages must add up to 100%.")
        else:
            if st.button("Save Budget Goals"):
                result = save_budget_goals(user_id, income, needs_percent, wants_percent, savings_percent)
                if result:
                    st.success("✅ Budget goals saved successfully!")
                else:
                    st.error("❌ Failed to save budget goals. Please try again.")
    else:
        st.error("User not found. Please check your email.")
