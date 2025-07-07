import streamlit as st
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="Login", page_icon="🔐")
st.title("🔐 Login")

# Email input
email_input = st.text_input("Enter your registered email")

if st.button("Login"):
    if not email_input:
        st.warning("⚠️ Please enter your email.")
    else:
        engine = get_engine()
        with engine.connect() as conn:
            query = text("SELECT * FROM users WHERE email = :email")
            result = conn.execute(query, {"email": email_input}).fetchone()

            if result:
                st.session_state["email"] = email_input
                st.success("✅ Login successful! Redirecting to Home...")
                st.switch_page("app.py")  # 👈 Navigate to Home page
            else:
                st.error("❌ Email not found. Please register first.")

# Optional: Show session email
if "email" in st.session_state:
    st.caption(f"📧 Currently logged in as: {st.session_state['email']}")
