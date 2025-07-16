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

def get_transactions_by_user(email):
    user = get_user_by_email(email)
    if not user or "id" not in user:
        return []
    user_id = user["id"]
    try:
        response = client.table("transactions").select("*").eq("user_id", user_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print("Error getting transactions:", e)
        return []

def get_budget_goals(user_id: str, created_at: str = None):
    try:
        query = supabase.table("budget_goals").select("*").eq("user_id", user_id)
        if created_at:
            query = query.eq("created_at", created_at)
        response = query.order("created_at", desc=True).limit(1).execute()

        if response.data:
            return response.data[0]
        else:
            return None
    except Exception as e:
        print("Error fetching budget goals:", e)
        return None

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

# Test Supabase connection
def test_connection():
    try:
        response = client.table("users").select("*").limit(1).execute()
        return "✅ Supabase connected successfully!" if response.data else "⚠️ Connected but no data."
    except Exception as e:
        return f"❌ Connection failed: {e}"
