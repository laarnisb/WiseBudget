import streamlit as st

st.set_page_config(page_title="Logout", page_icon="🚪")
st.title("🚪 Logout")

if "email" in st.session_state:
    user_email = st.session_state["email"]
    st.success(f"👋 {user_email}, you have been logged out.")
    st.session_state.clear()
else:
    st.info("You are not currently logged in.")

# Add a button to go back to Login or Home
st.page_link("pages/1_Login_Register.py", label="🔑 Go to Login Page", icon="↩️")
