import streamlit as st
from database import insert_user, client
from uuid import uuid4
from datetime import datetime
from passlib.hash import bcrypt

st.set_page_config(page_title="Register/Login", page_icon="🔐")
st.title("🔐 Register or Login")

# Create two tabs: Register and Login
tab_register, tab_login = st.tabs(["📝 Register", "🔐 Login"])

# ---------------- REGISTER TAB ---------------- #
with tab_register:
    st.subheader("📝 Create a New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if name and email and password:
            hashed_password = bcrypt.hash(password)
            uid = str(uuid4())

            result = insert_user(uid, name, email, hashed_password)

            if "error" in result:
                st.error(f"❌ Registration failed: {result['error']}")
            else:
                st.success("✅ Registration successful! You can now log in.")
        else:
            st.warning("Please fill in all fields.")

# ---------------- LOGIN TAB ---------------- #
with tab_login:
    st.subheader("🔐 Login to Your Account")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if login_email and login_password:
            try:
                response = client.table("users").select("*").eq("email", login_email).single().execute()
                if response.data:
                    stored_hash = response.data["password"]
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
