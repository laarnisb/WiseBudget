import streamlit as st
import pandas as pd
from database import insert_transactions

st.set_page_config(page_title="Upload Transactions", page_icon="📤")
st.title("📤 Upload Your Transactions")

# Ensure session email exists
if "email" not in st.session_state or not st.session_state.email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

email = st.session_state.email
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = {"description", "category", "amount", "date"}
        if not required_columns.issubset(df.columns):
            st.error("❌ The uploaded file must contain the following columns: "
                     "`description`, `category`, `amount`, `date`")
        else:
            # Normalize and clean category data
            df["category"] = df["category"].str.strip().str.lower()

            # Insert transactions for the current user
            insert_transactions(df, email)
            st.success("✅ Transactions uploaded successfully!")

    except Exception as e:
        st.error(f"❌ Error uploading transactions: {e}")
