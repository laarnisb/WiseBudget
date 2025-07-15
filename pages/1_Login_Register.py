import streamlit as st
from database import insert_user, authenticate_user
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Register/Login", page_icon="🔐")
tab1, tab2 = st.tabs(["Register", "Login"])

with tab1:
    st.header("Register New User")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not full_name or not email or not password:
            st.warning("Please complete all fields.")
        else:
            try:
                result = supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                user = result.user
                if user:
                    uid = user.id
                    db_response = insert_user(uid, full_name, email, password)
                    if "error" in db_response:
                        st.error(f"DB insert failed: {db_response['error']}")
                    else:
                        st.success("Registration successful. Please log in.")
                else:
                    st.error("Registration via Supabase failed.")
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.header("Login")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not login_email or not login_password:
            st.warning("Please enter your email and password.")
        else:
            response = authenticate_user(login_email, login_password)
            if "error" in response:
                st.error("Login failed.")
            else:
                st.success("Login successful.")
