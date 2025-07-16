import streamlit as st
from database import insert_user, get_user_by_email
from datetime import datetime
import bcrypt
import uuid

st.set_page_config(page_title="Login/Register", page_icon="🔐")
st.title("🔐 Login or Register")

# Initialize session state
if "email" not in st.session_state:
    st.session_state.email = None
if "name" not in st.session_state:
    st.session_state.name = None

# Sidebar welcome message
if st.session_state.email:
    st.sidebar.success(f"👋 Welcome, {st.session_state.name}!")

# Tabs for login and registration
tab_login, tab_register = st.tabs(["Login", "Register"])

# -------------------- Login Tab --------------------
with tab_login:
    st.header("Login to Your Account")
    st.info("New here? Please create an account using the **Register** tab.")

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        user = get_user_by_email(login_email)
        if user and bcrypt.checkpw(login_password.encode("utf-8"), user["password"].encode("utf-8")):
            st.session_state.email = user["email"]
            st.session_state.name = user["name"]
            st.success(f"Welcome back, {user['name']}! 👋")
            st.info("Use the sidebar to navigate through the app.")
        else:
            st.error("Invalid email or password.")

# -------------------- Register Tab --------------------
with tab_register:
    st.header("Create a New Account")

    name = st.text_input("Full Name", key="register_name")
    register_email = st.text_input("Email", key="register_email")
    register_password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register", key="register_button"):
        if name and register_email and register_password:
            existing_user = get_user_by_email(register_email)
            if existing_user:
                st.warning("⚠️ Email already registered. Please log in instead.")
            else:
                hashed_pw = bcrypt.hashpw(register_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                success = insert_user(name, register_email, hashed_pw, datetime.utcnow())

                if success is True:
                    st.success("✅ Registration successful. You can now log in.")
                else:
                    st.error("Registration failed. Please try again.")
        else:
            st.warning("Please fill in all fields.")
