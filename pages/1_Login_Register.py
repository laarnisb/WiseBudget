import streamlit as st
from database import insert_user, get_user_by_email
from datetime import datetime
import bcrypt

# Page setup
st.set_page_config(page_title="🔐 Register or Login", page_icon="🔐")
st.title("🔐 Register or Login")

# Initialize session state
if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "Register"
if "prefill_email" not in st.session_state:
    st.session_state.prefill_email = ""
if "login_notice" not in st.session_state:
    st.session_state.login_notice = ""

# Display two tabs: Register and Login
tabs = st.tabs(["Register", "Login"])

# Register tab
with tabs[0]:
    st.header("Create a New Account")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not full_name or not email or not password:
            st.warning("Please fill in all fields.")
        else:
            existing_user = get_user_by_email(email)
            if existing_user:
                # Email already exists: Redirect to login tab
                st.session_state.prefill_email = email
                st.session_state.login_notice = "This email is already registered. Please log in instead."
                st.session_state.auth_tab = "Login"
                st.experimental_rerun()
            else:
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                registration_date = datetime.utcnow().isoformat()
                try:
                    insert_user(full_name, email, hashed_pw, registration_date)
                    st.success("✅ User registered successfully!")
                except Exception as e:
                    st.error(f"❌ Registration failed: {str(e)}")

# Login tab
with tabs[1]:
    st.header("Login to Your Account")
    if st.session_state.login_notice:
        st.warning(st.session_state.login_notice)
        st.session_state.login_notice = ""

    login_email = st.text_input("Email", value=st.session_state.prefill_email, key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not login_email or not login_password:
            st.warning("Please enter both email and password.")
        else:
            user_record = get_user_by_email(login_email)
            if user_record:
                hashed_pw = user_record["password"]
                if bcrypt.checkpw(login_password.encode(), hashed_pw.encode()):
                    st.success(f"Welcome back, {user_record['name']}!")
                    st.session_state.email = login_email
                    st.session_state.name = user_record["name"]
                else:
                    st.error("Incorrect password. Please try again.")
            else:
                st.error("No user found with that email.")
