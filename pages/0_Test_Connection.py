import streamlit as st
from database import test_connection

st.set_page_config(page_title="🔌 Test Connection", page_icon="🔌")
st.title("🔌 Test Database Connection")

result = test_connection()
if result.startswith("✅"):
    st.success(result)
else:
    st.error(result)
