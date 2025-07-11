import streamlit as st
from database import insert_user
from datetime import datetime

st.set_page_config(page_title="Register", page_icon="📝")
st.title("📝 Register New User")

# Show form
with st.form("register_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submit = st.form_submit_button("Register")

# Handle form submission
if submit:
    if not name or not email:
        st.warning("⚠️ Please enter both name and email.")
    else:
        try:
            registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_user(name, email, registration_date)
            st.session_state["email"] = email  # 🔑 Save email to session
            st.success(f"✅ Registration successful! Welcome, {name}.")
        except ValueError as e:
            st.error(str(e))

# Optional: Show current session email (for debug)
if "email" in st.session_state:
    st.info(f"📧 Logged in as: {st.session_state['email']}")
