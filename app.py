import streamlit as st
from database import get_engine

# Page configuration
st.set_page_config(page_title="WiseBudget", layout="wide")

# App title and description
st.title("💸 Welcome to WiseBudget")

# Session-based email capture
if "email" not in st.session_state:
    st.session_state.email = ""

st.session_state.email = st.text_input("📧 Enter your registered email", value=st.session_state.email)

st.markdown("""
WiseBudget is your personal finance dashboard designed to help you:
- 📤 Upload and track your expenses
- 🎯 Set budget goals using the 50/30/20 rule
- 📈 Monitor your budget progress
- 📑 View detailed insights and summary reports

Use the sidebar to navigate between tools.
""")

# Optional horizontal rule
st.markdown("---")

# Trust notice
st.markdown("🔒 **Your data is private and encrypted.**")