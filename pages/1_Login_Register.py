# pages/1_Login_Register.py

import streamlit as st
from database import insert_user
from supabase import create_client
from datetime import datetime
import os

st.set_page_config(page_title="🔐 Login & Register", page_icon="🔐")
st.title("🔐 Login or Register")

# Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
client = create_client(url, key)

option = st.selectbox("Choose an option", ["Register", "Login"])

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

elif option == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            result = client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if result.user:
                st.success(f"✅ Logged in as {email}")
                st.session_state["email"] = email
            else:
                st.error("❌ Login failed.")

        except Exception as e:
            st.error(f"❌ Login error: {e}")
