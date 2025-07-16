import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- USERS ---

def insert_user(email, password, name):
    try:
        response = client.table("users").insert({
            "email": email,
            "password": password,
            "name": name
        }).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

def get_user_by_email(email):
    try:
        response = client.table("users").select("*").eq("email", email).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception:
        return None

def get_user_id_by_email(email):
    user = get_user_by_email(email)
    if isinstance(user, dict) and "id" in user:
        return user["id"]
    return None

# --- TRANSACTIONS ---

def insert_transactions(transactions):
    try:
        response = client.table("transactions").insert(transactions).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

def get_transactions_by_email(email):
    try:
        user = get_user_by_email(email)
        if not user:
            return []
        response = client.table("transactions").select("*").eq("user_id", user["id"]).execute()
        return response.data if response.data else []
    except Exception:
        return []

# Test Supabase connection
def test_connection():
    try:
        response = client.table("users").select("*").limit(1).execute()
        return "✅ Supabase connected successfully!" if response.data else "⚠️ Connected but no data."
    except Exception as e:
        return f"❌ Connection failed: {e}"
