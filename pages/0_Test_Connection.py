import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from database import test_connection

st.set_page_config(page_title="Test Connection", page_icon="🔌")
st.title("🔌 Test Database Connection")

try:
    result = test_connection()
    st.success(f"✅ Connection Successful! Server time: {result}")
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
