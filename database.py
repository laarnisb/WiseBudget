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
        response = client.table("users").select("id").limit(1).execute()
        if response.data:
            return "✅ Supabase connection successful."
        else:
            return "⚠️ Supabase connected, but no data found in 'users' table."
    except Exception as e:
        return f"❌ Supabase connection error: {str(e)}"

def insert_user(name, email, password):
    try:
        # Get authenticated user's UID
        user_info = client.auth.get_user()
        user_id = user_info.user.id

        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Prepare data for insert
        data = {
            "id": user_id,  # Matches Supabase Auth UID
            "name": name,
            "email": email,
            "password": hashed_pw,
            "registration_date": datetime.utcnow().isoformat()
        }

        # Insert user row
        response = client.table("users").insert(data).execute()

        if response.data:
            return True
        else:
            raise ValueError(f"❌ Failed to register user: {response}")
    except Exception as e:
        raise ValueError(f"❌ Unexpected error: {str(e)}")

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
