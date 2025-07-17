import streamlit as st
import hashlib
from database import get_user_by_email

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

def get_user_id_by_email(email):
    user = get_user_by_email(email)
    return user["id"] if user else None

def extract_month(date_str):
    try:
        return pd.to_datetime(date_str).strftime('%B %Y')
    except Exception as e:
        print("Error extracting month:", e)
        return "Unknown"
