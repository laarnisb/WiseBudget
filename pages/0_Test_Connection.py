import streamlit as st
from database import test_supabase_connection

st.set_page_config(page_title="🔌 Test Connection", page_icon="🔌")
st.title("🔌 Test Database Connection")

# Attempt to test the Supabase connection
result = test_supabase_connection()

# Display result
if result.startswith("✅"):
    st.success(result)
elif result.startswith("⚠️"):
    st.warning(result)
else:
    st.error(result)

# Footer
st.markdown("---")
st.markdown("Use this page to confirm the backend connection is working properly.")
