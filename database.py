from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
# USER FUNCTIONS
# -------------------------

def insert_user(email):
    try:
        existing_user = supabase.table("users").select("*").eq("email", email).execute()
        if existing_user.data:
            return existing_user.data[0]
        response = supabase.table("users").insert({"email": email}).execute()
        return response.data[0]
    except Exception as e:
        print("Error inserting user:", e)
        return None

def get_user_by_email(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print("Error getting user by email:", e)
        return None

# -------------------------
# TRANSACTION FUNCTIONS
# -------------------------

def insert_transactions(data):
    try:
        response = supabase.table("transactions").insert(data).execute()
        return response
    except Exception as e:
        print("Error inserting transactions:", e)
        return None

def fetch_transactions_by_user(user_id):
    try:
        response = supabase.table("transactions") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("date", desc=True) \
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print("Error fetching transactions:", e)
        return []

# -------------------------
# BUDGET GOAL FUNCTIONS
# -------------------------

def save_budget_goals(data):
    try:
        response = supabase.table("budget_goals").insert(data).execute()
        return response
    except Exception as e:
        print("Error saving budget goals:", e)
        return None

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

# -------------------------
# TEST CONNECTION
# -------------------------

def test_supabase_connection():
    try:
        response = supabase.table("users").select("*").limit(1).execute()
        if response.data is not None:
            return "✅ Supabase connected successfully!"
        else:
            return "⚠️ Supabase connected but no data found in 'users' table."
    except Exception as e:
        return f"❌ Supabase connection error: {str(e)}"
