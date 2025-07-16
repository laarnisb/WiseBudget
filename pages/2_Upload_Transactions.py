import streamlit as st
import pandas as pd
import time
from database import insert_transactions
from utils import get_user_id_by_email
from st_files_connection import FilesConnection

st.set_page_config(page_title="📤 Upload Transactions", page_icon="📤")
st.title("📤 Upload Transactions")

# Check if user is logged in
if "email" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

email = st.session_state["email"]
user_id = get_user_id_by_email(email)

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file to upload", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Check required columns
    required_columns = {"description", "category", "amount", "date"}
    if required_columns.issubset(df.columns):
        df["user_id"] = user_id
        df["email"] = email

        result = insert_transactions(df)

        if "error" not in result:
            st.success("✅ Transactions uploaded successfully!")
            st.info("You can now view them in the '📄 View Transactions' section from the sidebar.")
        else:
            st.error(f"❌ Failed to insert transactions: {result['error']}")
    else:
        st.error("❌ CSV must contain 'description', 'category', 'amount', and 'date' columns.")
