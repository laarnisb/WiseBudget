from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
# USER FUNCTIONS
# -------------------------

def insert_user(id, name, email, password):
    try:
        existing_user = supabase.table("users").select("*").eq("email", email).execute()
        if existing_user.data:
            return False  # Email already exists
        response = supabase.table("users").insert({
            "id": id,
            "name": name,
            "email": email,
            "password": password
        }).execute()
        return response.status_code == 201
    except Exception as e:
        print("Error inserting user:", e)
        return False

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

def insert_transaction(user_id, date, description, category, amount):
    try:
        response = supabase.table("transactions").insert([{
            "user_id": user_id,
            "date": date,
            "description": description,
            "category": category,
            "amount": amount
        }]).execute()
        return True
    except Exception as e:
        print("Error inserting transaction:", e)
        return False

def get_transactions_by_user(user_id):
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
# BUDGET GOALS FUNCTIONS
# -------------------------

def insert_budget_goals(user_id, income, needs_percent, wants_percent, savings_percent):
    try:
        response = supabase.table("budget_goals").insert([{
            "user_id": user_id,
            "income": income,
            "needs_percent": needs_percent,
            "wants_percent": wants_percent,
            "savings_percent": savings_percent
        }]).execute()
        return True
    except Exception as e:
        print("Error inserting budget goals:", e)
        return False

def get_budget_goals_by_user(user_id):
    try:
        response = supabase.table("budget_goals").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print("Error fetching budget goals:", e)
        return []

def fetch_budget_goals_by_user(user_id):
    try:
        response = supabase.table("budget_goals") \
            .select("needs_percent, wants_percent, savings_percent, income") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
        if response.data:
            return response.data[0]  # single dict
        return None
    except Exception as e:
        print("Error fetching budget goals:", e)
        return None

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
