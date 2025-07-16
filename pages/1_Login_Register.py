import streamlit as st
from database import insert_user, get_user_by_email
from datetime import datetime
import bcrypt
import uuid
import time

st.set_page_config(page_title="Login/Register", page_icon="🔐")

# -------------------- Page Title -------------------
st.title("🔐 Login or Register")

# Initialize session state
if "email" not in st.session_state:
    st.session_state.email = None
if "name" not in st.session_state:
    st.session_state.name = None

# Display sidebar message if logged in
if st.session_state.email:
    st.sidebar.success(f"Welcome, {st.session_state.name}!")

# Tabs: Login first, then Register
tab_login, tab_register = st.tabs(["Login", "Register"])

# -------------------- Login Tab --------------------
with tab_login:
    st.header("Login to Your Account")
    st.info("New here? Please create an account using the **Register** tab.")

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        user = get_user_by_email(login_email)
        # Check if user is valid and has a password field
        if isinstance(user, dict) and "password" in user:
            if bcrypt.checkpw(login_password.encode("utf-8"), user["password"].encode("utf-8")):
                st.session_state.email = user["email"]
                st.session_state.name = user["name"]
                st.session_state.just_logged_in = True
                time.sleep(2.5)
                st.rerun()
            else:
                st.error("Invalid email or password.")
        elif isinstance(user, dict) and "error" in user:
            st.error(f"Login failed: {user['error']}")
        else:
            st.error("User not found or data error.")
                       
# -------------------- End of Page --------------------
if st.session_state.get("just_logged_in"):
    st.info("Use the sidebar to navigate through the app.")
    del st.session_state["just_logged_in"]
   
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
            uid = str(uuid.uuid4())
            success = insert_user(uid, name, register_email, hashed_pw)
            if success:
                st.success("User registered successfully! You can now log in.")
            else:
                st.error("Registration failed. Please try again.")
