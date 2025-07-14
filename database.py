from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
import bcrypt
from supabase import create_client
from datetime import datetime

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create PostgreSQL and Supabase clients
engine = create_engine(DATABASE_URL)
client = create_client(SUPABASE_URL, SUPABASE_KEY)
client.postgrest.schema = "public"

def get_engine():
    return engine

def test_connection():
    with engine.connect() as conn:
        return conn.execute(text("SELECT NOW()")).scalar()

def insert_user(name, email, password, registration_date):
    try:
        if isinstance(password, str):
            password = password.encode('utf-8')
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        
        # Ensure registration_date is a datetime object
        if isinstance(registration_date, str):
            registration_date = datetime.fromisoformat(registration_date)

        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (name, email, password, registration_date) VALUES (:name, :email, :password, :date)"),
                {
                    "name": name,
                    "email": email,
                    "password": hashed_pw,
                    "date": registration_date
                }
            )
    except IntegrityError as e:
        if 'users_email_key' in str(e.orig):
            raise ValueError(f"⚠️ User with email '{email}' is already registered.")
        else:
            raise ValueError(f"❌ Failed to register user: {str(e)}")
    except Exception as e:
        raise ValueError(f"❌ Unexpected error: {str(e)}")

def get_user_by_email(email):
    response = client.table("users").select("*").eq("email", email).execute()
    if response.data:
        return response.data[0]  # Return user record as dictionary
    return None
