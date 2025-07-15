
import streamlit as st
import pandas as pd
import time
from database import insert_transactions
from utils import get_user_id_by_email
from st_files_connection import FilesConnection

st.set_page_config(page_title="📤 Upload Transactions", page_icon="📤")
st.title("📤 Upload Transactions")

if "email" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

email = st.session_state["email"]
user_id = get_user_id_by_email(email)

uploaded_file = st.file_uploader("Choose a CSV file to upload", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if {"description", "category", "amount", "date"}.issubset(df.columns):
        df["user_id"] = user_id
        df["email"] = email

        result = insert_transactions(df)

        if "error" not in result:
            st.success("✅ Transactions uploaded successfully!")
            time.sleep(2)
            st.switch_page("pages/3_View_Transactions.py")
        else:
            st.error(f"❌ Failed to insert transactions: {result['error']}")
    else:
        st.error("❌ CSV must contain 'description', 'category', 'amount', and 'date' columns.")
