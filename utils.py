import streamlit as st
import hashlib

def get_current_user_email():
    """Returns the current logged-in user's email from session state."""
    return st.session_state.get("email")

def login_user(email, password, user_record):
    """Check if email matches and password is valid (SHA256)."""
    if user_record is None:
        return False
    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    return user_record["email"] == email and user_record["password"] == hashed_input

def require_login():
    """Ensure the user is logged in; otherwise, stop the app."""
    if "email" not in st.session_state:
        st.warning("⚠️ Please log in to access this page.")
        st.stop()
    return st.session_state["email"]
