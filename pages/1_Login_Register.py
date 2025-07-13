import streamlit as st
from datetime import datetime
from database import insert_user, get_user_by_email
import bcrypt

st.set_page_config(page_title="Login/Register", page_icon="🔐")

# --- UI Display ---
st.title("🔐 Login / Register")

tab1, tab2 = st.tabs(["Login", "Register New User"])

# --- LOGIN TAB ---
with tab1:
    st.subheader("🔑 Login")

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = get_user_by_email(login_email)
        if user and bcrypt.checkpw(login_password.encode("utf-8"), user[3].encode("utf-8")):
            st.success(f"Welcome back, {user[1]}!")
            st.session_state["email"] = login_email
        else:
            st.error("❌ Invalid email or password.")

# --- REGISTER TAB ---
with tab2:
    st.subheader("📝 Register New User")

    reg_name = st.text_input("Full Name", key="reg_name")
    reg_email = st.text_input("Email", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Register"):
        if not reg_name or not reg_email or not reg_password:
            st.warning("⚠️ Please fill in all fields.")
        else:
            try:
                hashed_password = bcrypt.hashpw(reg_password.encode("utf-8"), bcrypt.gensalt())
                insert_user(reg_name, reg_email, hashed_password, datetime.now())
                st.success("✅ Registration successful! Please log in.")
            except ValueError as ve:
                st.error(str(ve))
            except Exception as e:
                st.error("❌ An unexpected error occurred during registration.")

# Optional horizontal rule and trust notice
st.markdown("---")
st.markdown("🔒 **Your data is private and encrypted.**")
