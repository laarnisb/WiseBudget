import streamlit as st
from database import test_connection
from database import client  # Import Supabase client from database.py

st.set_page_config(page_title="🔌 Test Connection", page_icon="🔌")
st.title("🔌 Test Database Connection")

# Test database (PostgreSQL via SQLAlchemy)
result = test_connection()
if result.startswith("✅"):
    st.success(result)
else:
    st.error(result)

# Test Supabase connection
def test_supabase_connection():
    try:
        response = client.table("users").select("*").limit(1).execute()
        if response.data is not None:
            st.success("✅ Supabase connected successfully!")
        else:
            st.warning("⚠️ Supabase connected but no data found in 'users' table.")
    except Exception as e:
        st.error(f"❌ Supabase connection error: {str(e)}")

# 🔁 Call the function so it runs
test_supabase_connection()

