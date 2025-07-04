# pages/1_Register_Users.py

import streamlit as st
from database import insert_user
from datetime import datetime

st.set_page_config(page_title="Register", page_icon="📝")
st.title("📝 Register New User")

# Use the email from session state
if "email" not in st.session_state:
    st.session_state.email = ""

name = st.text_input("Full Name")
email = st.text_input("Email", value=st.session_state.email)
register = st.button("Register")

if register:
    if not name or not email:
        st.warning("⚠️ Please enter both name and email.")
    else:
        try:
            insert_user(name, email, datetime.now())
            st.success("✅ User registered successfully!")
            st.session_state.email = email  # Update session email after registration
        except ValueError as e:
            st.error(str(e))
