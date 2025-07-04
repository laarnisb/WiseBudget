import streamlit as st
from database import insert_user
from datetime import datetime

st.set_page_config(page_title="Register", page_icon="📝")
st.title("📝 Register User")

st.write("Please enter your name and email to register.")

with st.form("register_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Register")

    if submitted:
        if not name or not email:
            st.warning("⚠️ Please enter both name and email.")
        else:
            try:
                insert_user(name, email, datetime.utcnow())
                st.success(f"✅ {name} has been registered successfully!")
            except ValueError as ve:
                st.error(str(ve))
