from supabase import create_client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_user(uid, name, email, password):
    registration_date = datetime.utcnow().isoformat()
    try:
        response = client.table("users").insert({
            "id": uid,
            "name": name,
            "email": email,
            "password": password,
            "registration_date": registration_date
        }).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

def authenticate_user(email, password):
    try:
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        return {"error": str(e)}

def test_connection():
    try:
        response = client.table("users").select("*").limit(1).execute()
        if response.data:
            return "✅ Supabase connected successfully!"
        else:
            return "⚠️ Supabase connected but no data found."
    except Exception as e:
        return f"❌ Connection failed: {e}"
