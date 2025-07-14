import streamlit as st
from datetime import datetime
import bcrypt
from database import insert_user, get_user_by_email
from supabase import create_client

# App config
st.set_page_config(page_title="Login/Register", page_icon="🔐")
st.title("🔐 Login or Register")

# Trust notice and visual separation
st.markdown("---")
st.markdown("🔒 **Your data is private and encrypted.**")

# Supabase setup using secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
client = create_client(SUPABASE_URL, SUPABASE_KEY)
client.postgrest.schema = "public"

# Session state for authentication
if "email" not in st.session_state:
    st.session_state.email = None

# Tabs for login and registration
tab1, tab2 = st.tabs(["🔓 Login", "📝 Register"])

# ----------------- Login Tab ----------------- #
with tab1:
    st.subheader("Login to Your Account")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = get_user_by_email(login_email)
        if user:
            hashed_pw = user["password"] if isinstance(user, dict) else user[3]
            if bcrypt.checkpw(login_password.encode(), hashed_pw.encode()):
                st.success("✅ Login successful!")
                st.session_state.email = login_email
                st.switch_page("Home.py")
            else:
                st.error("❌ Incorrect password.")
        else:
            st.warning("⚠️ Email not found. Please register.")

# ----------------- Register Tab ----------------- #
with tab2:
    st.subheader("Create a New Account")
    name = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Register"):
        if not name or not email or not password:
            st.warning("⚠️ All fields are required.")
        else:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            try:
                insert_user(name, email, hashed_password, datetime.now())
                st.success("✅ Registration successful. You can now log in.")
            except ValueError as e:
                st.error(str(e))
