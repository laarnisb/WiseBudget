import streamlit as st
import bcrypt
from database import insert_user, get_user_by_email
from datetime import datetime

st.set_page_config(page_title="Login or Register", page_icon="🔐")

tab1, tab2 = st.tabs(["Login", "Register"])

# -------------------- LOGIN --------------------
with tab1:
    st.header("🔑 Login")
    email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = get_user_by_email(email)

        if user:
            stored_hash = bytes.fromhex(user[3])  # user[3] is the hashed password in hex
            if bcrypt.checkpw(login_password.encode("utf-8"), stored_hash):
                st.success("Login successful!")
                st.session_state.email = email
                st.switch_page("Home.py")
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Invalid email or password.")

# -------------------- REGISTER --------------------
with tab2:
    st.header("📝 Register New User")

    name = st.text_input("Full Name")
    reg_email = st.text_input("Email")
    reg_password = st.text_input("Password", type="password")

    if st.button("Register"):
        try:
            # Check if email is already used
            if get_user_by_email(reg_email):
                st.warning("Email is already registered. Please log in.")
            else:
                hashed_password = bcrypt.hashpw(reg_password.encode("utf-8"), bcrypt.gensalt()).hex()
                date = datetime.utcnow()

                insert_user(name, reg_email, hashed_password, date)
                st.success("Registration successful! Please log in.")
        except Exception as e:
            st.error(f"An unexpected error occurred during registration.\n\n{e}")
