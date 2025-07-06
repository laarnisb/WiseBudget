import streamlit as st

def get_logged_in_user_email():
    """Return the currently logged-in user's email stored in session state."""
    return st.session_state.get("user_email", None)
