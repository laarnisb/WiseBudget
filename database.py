import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional, List
from datetime import datetime

# Load environment variables from .env if available
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------- USERS --------------------
def insert_user(name: str, email: str, password: str, created_at: datetime) -> bool:
    try:
        response = client.table("users").insert({
            "name": name,
            "email": email,
            "password": password,
            "created_at": created_at.isoformat()
        }).execute()
        return True if response.status_code == 201 else False
    except Exception as e:
        print(f"Error inserting user: {e}")
        return False

def get_user_by_email(email: str) -> Optional[dict]:
    try:
        response = client.table("users").select("*").eq("email", email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

# -------------------- TRANSACTIONS --------------------
def insert_transactions(transactions: List[dict]) -> bool:
    try:
        response = client.table("transactions").insert(transactions).execute()
        return True if response.status_code == 201 else False
    except Exception as e:
        print(f"Failed to insert transactions: {e}")
        return False

def get_transactions_by_user(email: str) -> List[dict]:
    try:
        response = client.table("transactions").select("*").eq("email", email).order("date", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []

# -------------------- TEST CONNECTION --------------------
def test_connection() -> str:
    try:
        response = client.table("users").select("*").limit(1).execute()
        if response.data is not None:
            return "✅ Supabase connected successfully!"
        else:
            return "⚠️ Supabase connected but no data found in 'users' table."
    except Exception as e:
        return f"❌ Supabase connection error: {str(e)}"
