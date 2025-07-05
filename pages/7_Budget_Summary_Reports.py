import streamlit as st
import pandas as pd
from database import get_connection, get_user_id

st.set_page_config(page_title="Budget Summary Reports", page_icon="🧾")
st.title("🧾 Budget Summary Reports")

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
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_id = %s
        GROUP BY category
    """, (user_id,))
    data = cursor.fetchall()
    if not data:
        st.warning("No transactions found for report.")
        st.stop()

    df = pd.DataFrame(data, columns=["Category", "Total Spent"])
    st.dataframe(df, use_container_width=True)

    st.subheader("Spending Distribution")
    st.plotly_chart(
        pd.DataFrame({"Amount": df["Total Spent"]}, index=df["Category"])
        .plot.pie(y="Amount", autopct="%.2f%%", figsize=(5, 5), legend=False)
        .figure
    )

except Exception as e:
    st.error(f"Error generating report: {e}")
finally:
    cursor.close()
