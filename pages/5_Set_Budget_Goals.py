import streamlit as st
from database import supabase, get_user_by_email
from datetime import datetime
import uuid

st.set_page_config(page_title="Set Budget Goals", page_icon="🎯")
st.title("🎯 Set Budget Goals")

# Session and user check
if "email" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

user = get_user_by_email(st.session_state["email"])
if not user:
    st.error("User not found.")
    st.stop()

user_id = user["id"]
current_month = datetime.now().strftime("%Y-%m")

st.info(f"Set your budget goals for {current_month}")

# Form for input
with st.form("budget_goals_form"):
    income = st.number_input("Monthly Income", min_value=0.0, format="%.2f", step=100.0)
    needs_percent = st.slider("Needs (%)", 0, 100, 50)
    wants_percent = st.slider("Wants (%)", 0, 100, 30)
    savings_percent = st.slider("Savings (%)", 0, 100, 20)
    submitted = st.form_submit_button("Save Budget Goals")

    if submitted:
        if needs_percent + wants_percent + savings_percent != 100:
            st.error("The total of Needs, Wants, and Savings must equal 100%.")
        else:
            # Optional: Check if record exists for current month and user
            existing = supabase.table("budget_goals").select("id").eq("user_id", user_id).eq("created_at", current_month).execute()

            data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "income": income,
                "needs_percent": needs_percent,
                "wants_percent": wants_percent,
                "savings_percent": savings_percent,
                "created_at": current_month
            }

            if existing.data:
                goal_id = existing.data[0]["id"]
                supabase.table("budget_goals").update(data).eq("id", goal_id).execute()
                st.success("Budget goals updated successfully!")
            else:
                supabase.table("budget_goals").insert(data).execute()
                st.success("Budget goals saved successfully!")
