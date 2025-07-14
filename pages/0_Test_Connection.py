import streamlit as st
from database import get_connection

st.set_page_config(page_title="🔌 DB Connection Test", page_icon="🔌")
st.title("🔌 Database Connection Test")

st.info("Testing connection to your Supabase PostgreSQL database...")

conn = get_connection()

if conn:
    try:
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()[0]
        st.success(f"✅ Connected successfully. Server time: {result}")
        cur.close()
    except Exception as e:
        st.error(f"⚠️ Query failed: {e}")
    finally:
        conn.close()
else:
    st.error("❌ Could not establish a database connection.")
