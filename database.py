from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import streamlit as st
import os
import pandas as pd

# TEMP: Hardcoded for local training/testing
DATABASE_URL = "postgresql://postgres.glgdvqapwjxjkxqfjpvz:tQUbHAfubF7J3PmD@aws-0-us-west-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)

def get_engine():
    return engine
    
def test_connection():
    """Test the connection to the database by returning the current timestamp."""
    with engine.connect() as conn:
        return conn.execute(text("SELECT NOW()")).scalar()

def insert_user(name, email, registration_date):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (name, email, registration_date) VALUES (:name, :email, :date)"),
                {"name": name, "email": email, "date": registration_date}
            )
    except IntegrityError as e:
        if 'users_email_key' in str(e.orig):
            raise ValueError(f"⚠️ User with email '{email}' is already registered.")
        else:
            raise ValueError(f"❌ Failed to register user: {str(e)}")

def insert_transactions(df: pd.DataFrame, user_email: str):
    engine = get_engine()
    with engine.connect() as conn:
        # Get user_id from users table
        result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": user_email})
        user_row = result.fetchone()
        if not user_row:
            raise ValueError(f"User with email {user_email} not found.")

        user_id = user_row[0]

        # Add user_id column to DataFrame
        df["user_id"] = user_id

        # Insert transactions
        for _, row in df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO transactions (date, description, category, amount, user_id)
                    VALUES (:date, :description, :category, :amount, :user_id)
                """),
                {
                    "date": row["date"],
                    "description": row["description"],
                    "category": row["category"],
                    "amount": row["amount"],
                    "user_id": row["user_id"]
                }
            )
        conn.commit()

def get_all_transactions():
    """Fetch all transaction records from the transactions table."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM transactions"))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

def add_user_email_column():
    """Add 'user_email' column to transactions table if it does not exist."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'transactions' AND column_name = 'user_email'
        """))
        if not result.fetchone():
            conn.execute(text("ALTER TABLE transactions ADD COLUMN user_email TEXT"))

def get_transactions_by_user(user_email: str) -> pd.DataFrame:
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT t.date, t.description, t.category, t.amount
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                WHERE u.email = :email
                ORDER BY t.date DESC
            """),
            {"email": user_email}
        )
        return pd.DataFrame(result.fetchall(), columns=result.keys())
