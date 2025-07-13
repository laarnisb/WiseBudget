import streamlit as st
from database import insert_user, get_user_by_email
from utils import login_user
from datetime import datetime

st.set_page_config(page_title="Login/Register", page_icon="🔐")
st.title("🔐 Login or Register")

tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

# LOGIN TAB
with tab1:
    st.subheader("🔑 Login")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if not login_email or not login_password:
            st.warning("Please enter both email and password.")
        else:
            user = get_user_by_email(login_email)
            if user and user["password"] == login_password:
                st.session_state.email = login_email
                st.success("✅ Login successful.")
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")

# REGISTER TAB
with tab2:
    st.subheader("📝 Register New User")
    reg_name = st.text_input("Full Name", key="reg_name")
    reg_email = st.text_input("Email", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Register"):
        if not reg_name or not reg_email or not reg_password:
            st.warning("All fields are required.")
        else:
            existing_user = get_user_by_email(reg_email)
            if existing_user:
                st.error("❌ This email is already registered.")
            else:
                insert_user(reg_name, reg_email, reg_password, datetime.now())
                st.success("✅ Registration successful. You are now logged in.")
                st.session_state.email = reg_email
                st.rerun()
