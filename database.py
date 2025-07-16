from supabase import create_client
import os

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------- USERS ----------------------
def insert_user(email, password):
    try:
        response = supabase.table("users").insert({"email": email, "password": password}).execute()
        return True if response.data else False
    except Exception as e:
        print("Error inserting user:", e)
        return False

def get_user_by_email(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print("Error fetching user by email:", e)
        return None

# ---------------------- TRANSACTIONS ----------------------
def insert_transaction(user_id, date, description, category, amount):
    try:
        response = supabase.table("transactions").insert({
            "user_id": user_id,
            "date": date,
            "description": description,
            "category": category,
            "amount": amount
        }).execute()
        return True if response.data else False
    except Exception as e:
        print("Error inserting transaction:", e)
        return False

def get_transactions_by_user(user_id):
    try:
        response = supabase.table("transactions") \
            .select("date, description, category, amount") \
            .eq("user_id", user_id) \
            .order("date", desc=True) \
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print("Error fetching transactions:", e)
        return []

# ---------------------- BUDGET GOALS ----------------------
def insert_budget_goals(user_id, income, needs_percent, wants_percent, savings_percent):
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
        print("Error inserting budget goals:", e)
        return False

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

# ---------------------- CONNECTION TEST ----------------------
def test_connection():
    try:
        response = supabase.table("users").select("*").limit(1).execute()
        if response.data is not None:
            return "✅ Supabase connection successful!"
        else:
            return "⚠️ Supabase connected but no user data found."
    except Exception as e:
        return f"❌ Connection failed: {e}"
