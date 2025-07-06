import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import streamlit as st

# Database connection setup using Streamlit secrets
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]
DB_NAME = st.secrets["DB_NAME"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# ✅ Fetch transactions by user
def get_transactions_by_user(user_email: str) -> pd.DataFrame:
    query = """
        SELECT description, category, amount, date
        FROM transactions
        WHERE user_email = %s
        ORDER BY date DESC;
    """
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn, params=(user_email,))
    return df

# ✅ Fetch budget goals by user
def get_budget_goals_by_user(user_email: str) -> pd.DataFrame:
    query = """
        SELECT needs, wants, savings
        FROM budget_goals
        WHERE user_email = %s
        ORDER BY created_at DESC
        LIMIT 1;
    """
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn, params=(user_email,))
    return df
