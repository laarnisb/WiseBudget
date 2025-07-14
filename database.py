import psycopg2
import streamlit as st
from datetime import datetime

# Load credentials from Streamlit secrets
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]
DB_NAME = st.secrets["DB_NAME"]

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Get a database connection
def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Insert a new user into the database
def insert_user(name, email, password, registration_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, email, password, registration_date)
        VALUES (%s, %s, %s, %s)
    """, (name, email, password, registration_date))
    conn.commit()
    conn.close()

# Fetch user by email
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE email = %s
    """, (email,))
    result = cursor.fetchone()
    conn.close()
    return result

# Insert a new transaction
def insert_transaction(user_email, date, category, description, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_email, date, category, description, amount)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_email, date, category, description, amount))
    conn.commit()
    conn.close()

# Retrieve transactions for a specific user
def get_transactions_by_user(user_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, category, description, amount
        FROM transactions
        WHERE user_email = %s
        ORDER BY date DESC;
    """, (user_email,))
    results = cursor.fetchall()
    conn.close()
    return results

# Insert or update a user's budget goal
def upsert_budget_goal(user_email, category, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budget_goals (user_email, category, amount)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_email, category)
        DO UPDATE SET amount = EXCLUDED.amount;
    """, (user_email, category, amount))
    conn.commit()
    conn.close()

# Retrieve budget goals for a user
def get_budget_goals(user_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, amount FROM budget_goals
        WHERE user_email = %s
    """, (user_email,))
    results = cursor.fetchall()
    conn.close()
    return results
