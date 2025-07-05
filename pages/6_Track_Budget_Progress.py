import streamlit as st
import pandas as pd
from database import get_connection, get_user_id

st.set_page_config(page_title="Track Budget Progress", page_icon="📈")
st.title("📈 Track Budget Progress")

email = st.session_state.get("user_email", None)
if email is None:
    st.warning("Please log in or set an email to continue.")
    st.stop()

user_id = get_user_id(email)
if user_id is None:
    st.warning("User not found.")
    st.stop()

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("""
        SELECT monthly_income, needs_percent, wants_percent, savings_percent
        FROM budget_goals
        WHERE user_id = %s
    """, (user_id,))
    goals = cursor.fetchone()
    if not goals:
        st.warning("No budget goals set.")
        st.stop()
    monthly_income, needs_pct, wants_pct, savings_pct = goals

    expected = {
        'Needs': round(monthly_income * needs_pct / 100, 2),
        'Wants': round(monthly_income * wants_pct / 100, 2),
        'Savings': round(monthly_income * savings_pct / 100, 2)
    }

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_id = %s
        GROUP BY category
    """, (user_id,))
    actual_data = dict(cursor.fetchall())

    actual = {
        'Needs': actual_data.get('Needs', 0),
        'Wants': actual_data.get('Wants', 0),
        'Savings': actual_data.get('Savings', 0)
    }

    df = pd.DataFrame({
        "Category": ["Needs", "Wants", "Savings"],
        "Expected ($)": list(expected.values()),
        "Actual ($)": list(actual.values())
    })

    st.subheader("Budget Comparison")
    st.dataframe(df, use_container_width=True)

    st.bar_chart(df.set_index("Category"))

except Exception as e:
    st.error(f"Error retrieving budget progress: {e}")
finally:
    cursor.close()
