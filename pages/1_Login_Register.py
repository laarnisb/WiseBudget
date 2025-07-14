
import streamlit as st
import bcrypt
from database import get_user_by_email

st.set_page_config(page_title="Login/Register", page_icon="🔐")

st.title("🔐 Login to Your Account")

login_email = st.text_input("Email", key="login_email")
login_password = st.text_input("Password", type="password", key="login_password")

if st.button("Login"):
    user = get_user_by_email(login_email)
    if user:
        hashed_pw = user['password']
        if hashed_pw:
            if bcrypt.checkpw(login_password.encode(), hashed_pw.encode()):
                st.success("Login successful!")
                st.session_state.email = login_email
                st.rerun()
            else:
                st.error("Incorrect password.")
        else:
            st.error("Password not found for this user.")
    else:
        st.error("No user found with that email.")
