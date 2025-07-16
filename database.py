import os
import uuid
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_user(email, password_hash, full_name):
    return supabase.table("users").insert({
        "id": str(uuid.uuid4()),
        "email": email,
        "password": password_hash,
        "full_name": full_name
    }).execute()

def get_user_by_email(email):
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None

def insert_transaction(payload):
    try:
        response = supabase.table("transactions").insert(payload).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

# ✅ This is the function needed by Upload Transactions page
def insert_transactions(transactions):
    try:
        response = supabase.table("transactions").insert(transactions).execute()
        return response
    except Exception as e:
        print("Error inserting transactions:", e)
        return {"error": str(e)}

# ✅ This is the dummy function needed by Track Budget Progress page
def get_engine():
    return None  # Not used, but included to prevent import error

def get_transactions_by_user(email):
    user = get_user_by_email(email)
    if not user:
        return []
    response = supabase.table("transactions").select("*").eq("user_id", user["id"]).order("date", desc=True).execute()
    return response.data

def fetch_transactions_by_month(user_id, month_str):
    try:
        response = supabase.table("transactions") \
            .select("*") \
            .eq("user_id", user_id) \
            .ilike("date", f"{month_str}-%") \
            .execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        print("Error fetching monthly transactions:", e)
        return pd.DataFrame()

def fetch_budget_goals_by_user(user_id):
    try:
        response = supabase.table("budget_goals") \
            .select("category, budget_amount") \
            .eq("user_id", user_id) \
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print("Error fetching budget goals:", e)
        return []

def insert_budget_goal(user_id, income, needs_percent, wants_percent, savings_percent):
    try:
        response = supabase.table("budget_goals").insert({
            "user_id": user_id,
            "income": income,
            "needs_percent": needs_percent,
            "wants_percent": wants_percent,
            "savings_percent": savings_percent
        }).execute()
        return True if response.data else False
    except Exception as e:
        print("Error inserting budget goal:", e)
        return False

def get_budget_goals_by_user(user_id):
    try:
        response = supabase.table("budget_goals") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print("Error fetching budget goals:", e)
        return []

def insert_budget_goals(goals_data):
    try:
        supabase.table("budget_goals").insert(goals_data).execute()
    except Exception as e:
        print("Error inserting budget goals:", e)
        raise

# Test Supabase connection
def test_connection():
    try:
        response = client.table("users").select("*").limit(1).execute()
        return "✅ Supabase connected successfully!" if response.data else "⚠️ Connected but no data."
    except Exception as e:
        return f"❌ Connection failed: {e}"
