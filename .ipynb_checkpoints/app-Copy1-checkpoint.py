import streamlit as st
import streamlit_authenticator as stauth
from database import get_engine
import yaml

st.set_page_config(page_title="WiseBudget", layout="wide")
st.title("💸 Welcome to WiseBudget")

st.markdown("""
WiseBudget is your personal finance dashboard designed to help you:
- Upload and track your expenses
- Set budget goals using the 50/30/20 rule
- Monitor your budget progress
- View detailed insights and summary reports

Use the sidebar to navigate between tools.
""")

st.markdown("---")
st.markdown("🔒 **Your data is private and encrypted.**")
