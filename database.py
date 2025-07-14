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
        # A simple fetch to test connection (e.g., from 'users' table)
        response = client.table("users").select("id").limit(1).execute()
        if response.status_code == 200:
            return "✅ Supabase connection successful."
        else:
            return f"❌ Supabase connection failed: {response.status_code} {response.data}"
    except Exception as e:
        return f"❌ Supabase connection error: {str(e)}"

def insert_user(name, email, password, registration_date):
    try:
        if isinstance(password, str):
            password = password.encode('utf-8')
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        if isinstance(registration_date, str):
            registration_date = datetime.fromisoformat(registration_date)

        data = {
            "name": name,
            "email": email,
            "password": hashed_pw,
            "registration_date": registration_date.isoformat()
        }

        response = client.table("users").insert(data).execute()

        if response.status_code == 201:
            return True
        elif response.status_code == 409:
            raise ValueError(f"⚠️ User with email '{email}' already exists.")
        else:
            raise ValueError(f"❌ Failed to register user: {response.data}")
    except Exception as e:
        raise ValueError(f"❌ Unexpected error: {str(e)}")

def get_user_by_email(email):
    try:
        response = client.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]  # Return user dictionary
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
