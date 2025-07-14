from supabase import create_client
from datetime import datetime
import os

# Environment variables (or hardcode securely during testing)
SUPABASE_URL = "https://glgdvqapwjxjkxqfjpvz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdsZ2R2cWFwd2p4amt4cWZqcHZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAwMTUwOTgsImV4cCI6MjA2NTU5MTA5OH0.9VyOu-eqXj3ZL3jtLGcKOFwh72sbeUa8WQ50CY-BAjA"

client = create_client(SUPABASE_URL, SUPABASE_KEY)
client.postgrest.schema = "public"

def insert_user(name, email, hashed_password, registration_date):
    """
    Inserts a new user into the users table.
    Password is expected as hex string.
    """
    try:
        result = client.table("users").insert({
            "name": name,
            "email": email,
            "password": hashed_password,
            "registration_date": registration_date.isoformat()  # Ensure correct timestamp format
        }).execute()
        return result
    except Exception as e:
        print(f"Insert error: {e}")
        raise

def get_user_by_email(email):
    """
    Retrieves a user row from the users table by email.
    Returns a tuple: (id, name, email, password, registration_date)
    """
    try:
        result = client.table("users").select("*").eq("email", email).limit(1).execute()
        if result.data:
            user = result.data[0]
            return (
                user.get("id"),
                user.get("name"),
                user.get("email"),
                user.get("password"),  # stored as hex string
                user.get("registration_date")
            )
        return None
    except Exception as e:
        print(f"Fetch error: {e}")
        raise
