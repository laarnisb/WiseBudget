import streamlit as st
import pandas as pd
from database import insert_transactions, get_user_by_email

st.set_page_config(page_title="📤 Upload Transactions", page_icon="📤")
st.title("📤 Upload Your Transactions")

# Only allow access if logged in
if not st.session_state.get("email"):
    st.warning("Please log in to upload transactions.")
    st.stop()

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = {"date", "description", "amount", "category"}
        if not required_columns.issubset(df.columns):
            st.error("CSV must contain columns: date, description, amount, category.")
        else:
            user_email = st.session_state.email
            user_id = get_user_id_by_email(user_email)

            if user_id:
                df["user_id"] = user_id
                insert_transactions(df)
                st.success("✅ Transactions uploaded successfully!")
                st.dataframe(df)
            else:
                st.error("❌ Could not find user ID for this email.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
