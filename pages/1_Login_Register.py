import streamlit as st
from database import insert_user, get_user_by_email
from datetime import datetime
import bcrypt

st.set_page_config(page_title="Login / Register", page_icon="🔐")
st.title("🔐 Login or Register")

# Session state for login
if "email" not in st.session_state:
    st.session_state.email = None

tabs = st.tabs(["Login", "Register"])

# --- Login Tab ---
with tabs[0]:
    st.subheader("Login")

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = get_user_by_email(login_email)
        if user and bcrypt.checkpw(login_password.encode("utf-8"), user["password"].encode("utf-8")):
            st.success("Login successful!")
            st.session_state.email = login_email
            st.switch_page("Home.py")
        else:
            st.error("Invalid email or password.")

# --- Register Tab ---
with tabs[1]:
    st.subheader("Register New User")

    name = st.text_input("Full Name", key="register_name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        if not name or not email or not password:
            st.warning("Please fill in all fields.")
        else:
            try:
                insert_user(name, email, password, datetime.now())
                st.success("Registration successful! Please log in.")
            except ValueError as ve:
                st.error(str(ve))
