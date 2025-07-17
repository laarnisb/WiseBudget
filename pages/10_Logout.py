import streamlit as st

st.set_page_config(page_title="Logout", page_icon="🚪")
st.title("🚪 Logout")

if "name" in st.session_state:
    user_name = st.session_state["name"]
    st.success(f"👋 {user_name}, you have been logged out.")
    st.session_state.clear()
else:
    st.info("You are not currently logged in.")

# Go back to login
st.page_link("pages/1_Login_Register.py", label="🔑 Go to Login Page", icon="↩️")
