import streamlit as st

def get_current_user_email():
    """Returns the current logged-in user's email from session state."""
    return st.session_state.get("email")
