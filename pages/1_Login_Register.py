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
with tab2:
    st.subheader("Create New Account")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if full_name and email and password:
            try:
                # Step 1: Sign up using Supabase Auth
                auth_response = client.auth.sign_up({
                    "email": email,
                    "password": password
                })

                if auth_response.user:
                    # Step 2: Add metadata to 'users' table
                    from datetime import datetime
                    import uuid

                    user_id = str(uuid.uuid4())  # You can also use auth_response.user.id if preferred
                    registration_date = datetime.utcnow().isoformat()

                    insert_response = client.table("users").insert({
                        "id": user_id,
                        "name": full_name,
                        "email": email,
                        "registration_date": registration_date
                    }).execute()

                    st.success("✅ Registration successful! Please check your email to confirm your account.")
                else:
                    st.error("❌ Failed to register. Check your email/password or try again.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all fields.")
