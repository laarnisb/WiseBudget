import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="View Transactions", page_icon="📄")
st.title("📄 View Transactions")

st.write("Enter your registered email to view your transactions.")

email = st.text_input("Email")

if email:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            # Retrieve user_id
            user_query = text("SELECT id FROM users WHERE email = :email")
            user_result = conn.execute(user_query, {"email": email}).fetchone()

            if user_result:
                user_id = user_result[0]

                # Retrieve transactions for this user
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
                    st.subheader("📋 Transaction History")
                    st.dataframe(df)

            else:
                st.warning("⚠️ No user found with that email.")
    except Exception as e:
        st.error(f"❌ Error loading transactions: {e}")
