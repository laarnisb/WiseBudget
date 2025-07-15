from supabase import create_client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_user(uid, name, email, password):
    registration_date = datetime.utcnow().isoformat()
    try:
        response = supabase.table("users").insert({
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
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        return {"error": str(e)}
