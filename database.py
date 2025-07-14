import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st

# Use DATABASE_URL from Streamlit secrets
DATABASE_URL = st.secrets["DATABASE_URL"]

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)


# Insert a new user (registration)
def insert_user(name: str, email: str, hashed_password: str):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (name, email, password) VALUES (:name, :email, :password)"),
                {"name": name, "email": email, "password": hashed_password}
            )
        return True
    except Exception as e:
        print("Error inserting user:", e)
        return False


# Get user by email (for login)
def get_user_by_email(email: str):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email}
        )
        return result.fetchone()


# Insert uploaded transactions for a specific user
def insert_transactions(df: pd.DataFrame, user_email: str):
    with engine.begin() as conn:
        # Fetch user ID
        result = conn.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": user_email}
        )
        user_row = result.fetchone()
        if not user_row:
            raise ValueError(f"User with email {user_email} not found.")
        user_id = user_row[0]
        df["user_id"] = user_id

        # Insert each transaction
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


# Get all transactions for a specific user
def get_transactions_by_email(user_email: str):
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
        return result.fetchall()
