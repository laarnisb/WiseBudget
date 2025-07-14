from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import pandas as pd
import streamlit as st

DATABASE_URL = st.secrets["DATABASE_URL"]
engine = create_engine(DATABASE_URL)

def get_engine():
    return engine

def test_connection():
    with engine.connect() as conn:
        return conn.execute(text("SELECT NOW()")).scalar()

def insert_user(name, email, password_hash, registration_date):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (name, email, password, registration_date) VALUES (:name, :email, :password, :date)"),
                {"name": name, "email": email, "password": password_hash, "date": registration_date}
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

def insert_transactions(df: pd.DataFrame, user_email: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": user_email})
        user_row = result.fetchone()
        if not user_row:
            raise ValueError(f"User with email {user_email} not found.")
        user_id = user_row[0]
        df["user_id"] = user_id

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
