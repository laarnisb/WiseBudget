import streamlit as st
from database import insert_user, get_user_by_email
from datetime import datetime
import bcrypt

st.set_page_config(page_title="Login/Register", page_icon="🔐")

# -------------------- Page Title --------------------
st.title("🔐 Login or Register")

# Initialize session state
if "email" not in st.session_state:
    st.session_state.email = None
if "name" not in st.session_state:
    st.session_state.name = None

# Display sidebar message if logged in
if st.session_state.email:
    st.sidebar.success(f"👋 Welcome, {st.session_state.name}!")

# Tabs: Login first, then Register
tab_login, tab_register = st.tabs(["Login", "Register"])

# -------------------- Login Tab --------------------
with tab_login:
    st.subheader("Login to Your Account")
    st.info("New here? Please create an account using the **Register** tab.")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            st.session_state["user"] = user
            st.session_state["email"] = user["email"]
            st.session_state["name"] = user["name"]

            # Auto-clear fields
            st.session_state["login_email"] = ""
            st.session_state["login_password"] = ""

            st.success(f"Welcome back, {user['name']}! 👋")
            st.info("Use the sidebar to navigate through the app.")
        else:
            st.error("Invalid email or password. Please try again.")

# -------------------- Register Tab --------------------
with tab_register:
    st.subheader("📝 Create a New Account")

    name = st.text_input("Full Name", key="register_name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        if get_user_by_email(email):
            st.error("An account with this email already exists. Please log in instead.")
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            success = insert_user(name, email, hashed_pw, datetime.utcnow())
            if success:
                # Auto-clear fields after registration
                st.session_state["register_name"] = ""
                st.session_state["register_email"] = ""
                st.session_state["register_password"] = ""

                st.success("Account created successfully! You can now log in.")
            else:
                st.error("There was an error creating your account. Please try again.")
