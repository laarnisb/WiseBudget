from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load SUPABASE_URL and SUPABASE_KEY from .env if available

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_user(name, email, password, created_at):
    try:
        response = supabase.table("users").insert({
            "name": name,
            "email": email,
            "password": password,
            "created_at": created_at
        }).execute()
        print("Insert response:", response)
        return response.status_code == 201
    except Exception as e:
        print("Insert user error:", e)
        return False

def get_user_by_email(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).single().execute()
        if response.data:
            return response.data
        return None
    except Exception as e:
        print("Get user error:", e)
        return None

def test_connection():
    try:
        response = supabase.table("users").select("*").limit(1).execute()
        if response.data is not None:
            return "✅ Supabase connection successful!"
        else:
            return "⚠️ Supabase connected but no data found in 'users' table."
    except Exception as e:
        return f"❌ Supabase connection failed: {str(e)}"
