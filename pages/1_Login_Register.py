# pages/1_Login_Register.py

import streamlit as st
from database import insert_user, get_user_by_email
import uuid
import bcrypt
from datetime import datetime

st.set_page_config(page_title="Login or Register", page_icon="🔐")

# Define tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

# --- LOGIN TAB ---
with tab_login:
    st.subheader("Login to Your Account")
    st.info("New here? Please register an account using the **Register** tab.")

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = get_user_by_email(login_email)
        if user:
            stored_hashed = user['password'].encode('utf-8')
            entered_password = login_password.encode('utf-8')

            if bcrypt.checkpw(entered_password, stored_hashed):
                st.success("✅ Login successful!")
                st.session_state.email = login_email
                st.rerun()
            else:
                st.error("❌ Incorrect password.")
        else:
            st.warning("⚠️ Email not found. Please register first.")

# --- REGISTER TAB ---
with tab_register:
    st.subheader("📝 Register New Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        if name and email and password:
            existing_user = get_user_by_email(email)
            if existing_user:
                st.warning("⚠️ Email already registered. Please login.")
            else:
                hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                uid = str(uuid.uuid4())
                result = insert_user(uid, name, email, hashed_pw)
                if "error" in result:
                    st.error(f"DB insert failed: {result['error']}")
                else:
                    st.success("✅ Registered successfully! Please login.")
                    st.session_state.email = email
        else:
            st.warning("⚠️ Please fill in all fields.")
