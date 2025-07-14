# database.py

import psycopg2
import streamlit as st
from psycopg2.extras import RealDictCursor

# Get DB connection using Streamlit secrets
def get_connection():
    try:
        DATABASE_URL = st.secrets["DATABASE_URL"]
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    except KeyError:
        st.error("❌ DATABASE_URL not found in Streamlit secrets.")
        raise
    except psycopg2.OperationalError as e:
        st.error(f"❌ Failed to connect to the database: {e}")
        raise

# Sample query functions
def insert_user(name, email, password, registration_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password, registration_date) VALUES (%s, %s, %s, %s)",
        (name, email, password, registration_date),
    )
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def get_transactions_by_user(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE email = %s", (email,))
    transactions = cur.fetchall()
    cur.close()
    conn.close()
    return transactions
