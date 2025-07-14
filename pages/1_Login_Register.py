import streamlit as st
from database import insert_user
from supabase import create_client
import os

# Initialize Supabase client
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        try:
            auth_response = client.auth.sign_in_with_password(
                {"email": login_email, "password": login_password}
            )
            if auth_response.user:
                st.success("Login successful!")
                st.session_state.email = login_email
                st.switch_page("Home.py")
            else:
                st.error("Invalid email or password.")
        except Exception as e:
            st.error(f"❌ Login failed: {str(e)}")

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
                insert_user(name, email, password)
                st.success("Registration successful! Please log in.")
            except ValueError as ve:
                st.error(str(ve))
