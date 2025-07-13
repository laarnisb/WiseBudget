from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
import bcrypt

# Load .env variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_engine():
    return engine

def test_connection():
    with engine.connect() as conn:
        return conn.execute(text("SELECT NOW()")).scalar()

def insert_user(name, email, password, registration_date):
    try:
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (name, email, password, registration_date) VALUES (:name, :email, :password, :date)"),
                {"name": name, "email": email, "password": hashed_pw, "date": registration_date}
            )
    except IntegrityError as e:
        if 'users_email_key' in str(e.orig):
            raise ValueError(f"⚠️ User with email '{email}' is already registered.")
        else:
            raise ValueError(f"❌ Failed to register user: {str(e)}")

def get_user_by_email(email):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})
        return result.fetchone()
