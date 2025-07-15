import streamlit as st
from database import insert_user
from supabase import create_client
from datetime import datetime
import os
from passlib.hash import bcrypt

# Page configuration
st.set_page_config(page_title="🔐 Login & Register", page_icon="🔐")
st.title("🔐 Login or Register")

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Option selector
option = st.selectbox("Choose an option", ["Register", "Login"])

# Registration logic
if option == "Register":
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not name or not email or not password:
            st.warning("Please fill in all fields.")
        else:
            try:
                result = client.auth.sign_up({
                    "email": email,
                    "password": password
                })

                if result.user:
                    uid = result.user.id
                    response = insert_user(uid, name, email, password)

                    if "error" in response:
                        st.error(f"DB insert failed: {response['error']}")
                    else:
                        st.success("✅ User registered successfully!")
                else:
                    st.error("❌ Registration failed. No user object returned.")

            except Exception as e:
                st.error(f"❌ Registration error: {e}")

# Login logic
elif page == "Login":
    st.subheader("🔐 Login to Your Account")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if login_email and login_password:
            try:
                # Fetch user record by email
                response = client.table("users").select("*").eq("email", login_email).single().execute()
                if response.data:
                    stored_hash = response.data["password"]
                    # Compare hashed password
                    if bcrypt.verify(login_password, stored_hash):
                        st.success(f"Welcome back, {response.data['name']}!")
                        st.session_state.email = login_email
                    else:
                        st.error("❌ Incorrect password.")
                else:
                    st.error("❌ No user found with this email.")
            except Exception as e:
                st.error(f"❌ Login failed: {str(e)}")
        else:
            st.warning("Please enter both email and password.")
