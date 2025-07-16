import streamlit as st
from database import insert_user, get_user_by_email
from datetime import datetime
import bcrypt

st.set_page_config(page_title="Login/Register", page_icon="🔐")

# Initialize session state
if "email" not in st.session_state:
    st.session_state.email = None

# -------------------- Page Title --------------------
st.title("🔐 Login or Register")

# Tabs: Login first, then Register
tab_login, tab_register = st.tabs(["Login", "Register"])

# -------------------- Login Tab --------------------
with tab_login:
    st.header("Login to Your Account")

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        user = get_user_by_email(login_email)
        if user and bcrypt.checkpw(login_password.encode("utf-8"), user["password"].encode("utf-8")):
            st.session_state.email = user["email"]
            st.success(f"Welcome back, {user['name']}!")
            st.experimental_rerun()  # Ensure session state is updated before redirect
            st.switch_page("pages/3_View_Transactions.py")
        else:
            st.error("Invalid email or password.")

    st.info("New here? Please create an account using the **Register** tab.")

# -------------------- Register Tab --------------------
with tab_register:
    st.header("Register a New Account")

    name = st.text_input("Full Name", key="register_name")
    register_email = st.text_input("Email", key="register_email")
    register_password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register", key="register_button"):
        existing_user = get_user_by_email(register_email)
        if existing_user:
            st.warning("Email already registered. Please log in instead.")
        else:
            hashed_pw = bcrypt.hashpw(register_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            success = insert_user(name, register_email, hashed_pw, datetime.utcnow())
            if success:
                st.success("User registered successfully! You can now log in.")
            else:
                st.error("Registration failed. Please try again.")
