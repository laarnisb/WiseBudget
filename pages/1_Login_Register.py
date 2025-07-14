import streamlit as st
import bcrypt
from database import get_user_by_email, insert_user
from datetime import datetime

st.set_page_config(page_title="Login / Register", page_icon="🔐")

st.title("🔐 Login or 📝 Register")

tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

# --- LOGIN TAB ---
with tab1:
    st.subheader("Login to Your Account")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = get_user_by_email(login_email)
        if user:
            hashed_pw = user[4]  # assuming password is at index 4
            if bcrypt.checkpw(login_password.encode(), hashed_pw.encode()):
                st.session_state.email = login_email
                st.success("Login successful!")
                st.switch_page("Home.py")
            else:
                st.error("Incorrect password.")
        else:
            st.error("User not found.")

# --- REGISTER TAB ---
with tab2:
    st.subheader("Register a New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        if not all([name, email, password]):
            st.warning("Please fill out all fields.")
        elif get_user_by_email(email):
            st.error("Email is already registered.")
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            insert_user(name, email, hashed_pw, datetime.utcnow())
            st.success("Registration successful. You can now log in.")
            st.experimental_rerun()
