import streamlit as st
from database import get_engine

# Optional: import authenticator if you plan to add login
# import streamlit_authenticator as stauth
# import yaml

# Page configuration
st.set_page_config(page_title="WiseBudget", layout="wide")

# App title and description
st.title("💸 Welcome to WiseBudget")

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
