import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Register & Login", page_icon="🔐")
st.title("🔐 Register or Login")

# Define tabs
tab1, tab2 = st.tabs(["Register New User", "Login"])

with tab1:
    elif choice == "Register":
    st.subheader("Register New User")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not full_name or not email or not password:
            st.warning("Please fill in all fields.")
        else:
            try:
                # Step 1: Sign up to Supabase Auth
                result = supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })

                user = result.user
                if user is not None:
                    uid = user.id

                    # Step 2: Insert into users table
                    db_response = insert_user(uid, full_name, email, password)
                    if "error" in db_response:
                        st.error(f"Failed to insert user into database: {db_response['error']}")
                    else:
                        st.success("Registration successful! Please log in.")
                else:
                    st.error("Supabase Auth registration failed.")

            except Exception as e:
                st.error(f"Unexpected error during registration: {e}")
    
with tab2:
    st.subheader("Login")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not login_email or not login_password:
            st.error("Please enter both email and password.")
        else:
            try:
                user = client.auth.sign_in_with_password({
                    "email": login_email,
                    "password": login_password
                })
                st.session_state["email"] = login_email
                st.success("Login successful!")
                st.experimental_rerun()
            except Exception as e:
                st.error("Login failed: Invalid login credentials")
