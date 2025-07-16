# database.py

from supabase import create_client  # Supabase client for database and auth
from datetime import datetime       # Used for generating registration timestamp
import os
from dotenv import load_dotenv      # Load environment variables securely from .env
from passlib.hash import bcrypt     # For checking password hashes

# Load the .env file to access SUPABASE_URL and SUPABASE_KEY
load_dotenv()

# Retrieve Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Insert a new user into the 'users' table with hashed password already provided
def insert_user(uid, name, email, password):
    registration_date = datetime.utcnow().isoformat()
    try:
        response = client.table("users").insert({
            "id": uid,
            "name": name,
            "email": email,
            "password": password,  # Already hashed before calling this function
            "registration_date": registration_date
        }).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

# Check if a user already exists by email
def get_user_by_email(email):
    try:
        response = client.table("users").select("*").eq("email", email).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        return {"error": str(e)}

# Placeholder insert_transactions function
def insert_transactions(data):
    try:
        response = client.table("transactions").insert(data).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

# Test Supabase connection
def test_connection():
    try:
        response = client.table("users").select("*").limit(1).execute()
        return "✅ Supabase connected successfully!" if response.data else "⚠️ Connected but no data."
    except Exception as e:
        return f"❌ Connection failed: {e}"
