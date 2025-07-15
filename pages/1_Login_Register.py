import streamlit as st
from database import insert_user, authenticate_user, get_user_by_email
import uuid

st.set_page_config(page_title="Login/Register", page_icon="🔐")
st.title("🔐 Login or Register")

# Use two tabs instead of dropdown
tab1, tab2 = st.tabs(["Register", "Login"])

with tab1:
    st.subheader("Create New Account")
    name = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    register_btn = st.button("Register")

    if register_btn:
        if name and email and password:
            # Check if the email already exists
            existing_user = get_user_by_email(email)
            if existing_user:
                st.warning("⚠️ Email already registered. Please proceed to login.")
            else:
                uid = str(uuid.uuid4())
                response = insert_user(uid, name, email, password)
                if "error" in response:
                    st.error(f"Registration failed: {response['error']}")
                else:
                    st.success("✅ Registration successful. You can now log in.")
        else:
            st.warning("Please fill in all fields.")

with tab2:
    st.subheader("Login to Your Account")
    email = st.text_input("Email", key="log_email")
    password = st.text_input("Password", type="password", key="log_password")
    login_btn = st.button("Login")

    if login_btn:
        if email and password:
            response = authenticate_user(email, password)
            if "error" in response:
                st.error("❌ Login failed. Please check your credentials.")
            else:
                st.success("✅ Login successful.")
                st.session_state["email"] = email
        else:
            st.warning("Please enter both email and password.")
