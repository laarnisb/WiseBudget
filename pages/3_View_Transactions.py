import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="View Transactions", page_icon="📋")
st.title("📋 View Transactions")

st.write("Enter your registered email to view your uploaded transactions.")

email = st.text_input("Email")

if email:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            # Step 1: Fetch user_id
            user_query = text("SELECT id FROM users WHERE email = :email")
            user_result = conn.execute(user_query, {"email": email}).fetchone()

            if user_result:
                user_id = user_result[0]

                # Step 2: Fetch transactions
                txn_query = text("""
                    SELECT amount, category, description, date
                    FROM transactions
                    WHERE user_id = :user_id
                    ORDER BY date DESC
                """)
                df = pd.read_sql(txn_query, conn, params={"user_id": user_id})

                if df.empty:
                    st.info("ℹ️ No transactions found for this user.")
                else:
                    st.subheader("🧾 Your Transactions")
                    st.dataframe(df)

            else:
                st.warning("⚠️ No user found with that email.")
    except Exception as e:
        st.error(f"❌ Error loading transactions: {e}")
