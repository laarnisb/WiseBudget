from supabase import create_client  # Supabase client for database and auth
from datetime import datetime       # Used for generating registration timestamp
import os
from dotenv import load_dotenv      # Load environment variables securely from .env
from passlib.hash import bcrypt

# Load the .env file to access SUPABASE_URL and SUPABASE_KEY
load_dotenv()

# Retrieve Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client for database operations and authentication
client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to insert a new user into the 'users' table
def insert_user(uid, name, email, password):
    from datetime import datetime
    registration_date = datetime.utcnow().isoformat()

    # Hash the password before storing
    hashed_password = bcrypt.hash(password)

    try:
        response = client.table("users").insert({
            "id": uid,
            "name": name,
            "email": email,
            "password": hashed_password,
            "registration_date": registration_date
        }).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

# Function to authenticate a user using Supabase Auth
def authenticate_user(email, password):
    try:
        # Attempt to sign in with email and password
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        # Return error details if authentication fails
        return {"error": str(e)}

# Function to test the connection to Supabase
def test_connection():
    try:
        # Attempt to retrieve a single row from 'users' to confirm connectivity
        response = client.table("users").select("*").limit(1).execute()
        if response.data:
            return "✅ Supabase connected successfully!"
        else:
            return "⚠️ Supabase connected but no data found."
    except Exception as e:
        # Return error if connection test fails
        return f"❌ Connection failed: {e}"
