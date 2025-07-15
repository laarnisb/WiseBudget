from supabase import create_client
import streamlit as st
import bcrypt
from datetime import datetime

# Load secrets from Streamlit settings
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Create Supabase client
client = create_client(SUPABASE_URL, SUPABASE_KEY)
client.postgrest.schema = "public"

def test_connection():
    try:
        result = client.table("users").select("*").limit(1).execute()
        if result.data:
            return "✅ Supabase connected and data fetched."
        else:
            return "⚠️ Supabase connected but no data in 'users' table."
    except Exception as e:
        return f"❌ Supabase connection error: {e}"

import uuid
from datetime import datetime

def insert_user(full_name, email, password):
    id = str(uuid.uuid4())  # Generate a unique UUID
    registration_date = datetime.utcnow().isoformat()  # Current UTC time

    data = {
        "id": id,
        "name": full_name,
        "email": email,
        "password": password,
        "registration_date": registration_date,
    }

    try:
        response = supabase.table("users").insert(data).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

def get_user_by_email(email):
    try:
        response = client.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        raise ValueError(f"❌ Failed to fetch user: {str(e)}")

def get_transactions_by_user(email):
    try:
        response = client.table("transactions").select("*").eq("email", email).execute()
        if response.data:
            return response.data
        return []
    except Exception as e:
        raise ValueError(f"❌ Failed to fetch transactions: {str(e)}")
