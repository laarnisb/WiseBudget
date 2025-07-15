
import streamlit as st
from database import insert_user, get_user_by_email
import bcrypt
from datetime import datetime

st.set_page_config(page_title="🔐 Login or Register", page_icon="🔐")

# Title
st.title("🔐 Login or Register")

# Tabs for Login and Register
tabs = st.tabs(["Login", "Register"])

with tabs[0]:
    st.subheader("Login to Your Account")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = get_user_by_email(login_email)
        if user and bcrypt.checkpw(login_password.encode("utf-8"), user["password"].encode("utf-8")):
            st.success(f"Welcome back, {user['name']}!")
            st.session_state.email = login_email
            st.rerun()
        else:
            st.error("Invalid email or password.")

    st.info("New here? Please create an account using the **Register** tab.")

with tabs[1]:
    st.subheader("Create an Account")
    name = st.text_input("Full Name", key="register_name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        user = get_user_by_email(email)
        if user:
            st.info("Email is already registered. Please proceed to login.")
        else:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            result = insert_user(name, email, hashed_password, datetime.utcnow().isoformat())
            if result == "Success":
                st.success("✅ User registered successfully! You can now login.")
            else:
                st.error(f"❌ Registration failed: {result}")
