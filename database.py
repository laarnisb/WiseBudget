from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import streamlit as st
import pandas as pd

engine = create_engine(st.secrets["DATABASE_URL"])

def get_engine():
    return create_engine(st.secrets["DATABASE_URL"])

def insert_user(name, email, registration_date):
    try:
        engine = get_engine()
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

def normalize_category(category):
    category = str(category).lower()
    if "grocer" in category:
        return "Groceries"
    elif "trans" in category or "uber" in category:
        return "Transport"
    elif "rent" in category or "mortgage" in category:
        return "Housing"
    elif "utilit" in category or "electric" in category:
        return "Utilities"
    elif "entertain" in category or "netflix" in category:
        return "Entertainment"
    elif "salary" in category or "income" in category:
        return "Income"
    elif "dining" in category or "restaurant" in category:
        return "Dining"
    else:
        return "Other"

def insert_transactions(df: pd.DataFrame):
    with engine.begin() as conn:
        for _, row in df.iterrows():
            result = conn.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": row["user_email"]}
            )
            user_row = result.fetchone()
            if not user_row:
                raise ValueError(f"❌ User with email '{row['user_email']}' not found.")
            user_id = user_row[0]
            category = normalize_category(row["category"])
            conn.execute(
                text("""
                    INSERT INTO transactions (user_id, amount, category, description, date)
                    VALUES (:user_id, :amount, :category, :description, :date)
                """),
                {
                    "user_id": user_id,
                    "amount": row["amount"],
                    "category": category,
                    "description": row["description"],
                    "date": row["date"]
                }
            )

# ✅ Unified naming: This works with pages/6_Track_Budget_Progress.py
def get_transactions_by_user(user_email: str) -> pd.DataFrame:
    return get_transactions_by_email(user_email)

# ✅ Original working query
def get_transactions_by_email(email):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT t.date, t.description, t.category, t.amount
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                WHERE u.email = :email
                ORDER BY t.date DESC
            """),
            {"email": email}
        )
        return pd.DataFrame(result.fetchall(), columns=result.keys())

# ✅ Budget goals for use in budget tracking page
def get_budget_goals_by_user(user_email: str) -> pd.DataFrame:
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT needs, wants, savings
                FROM budget_goals
                WHERE user_email = :email
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"email": user_email}
        )
        return pd.DataFrame(result.fetchall(), columns=result.keys())
