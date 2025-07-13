import streamlit as st
import pandas as pd
from database import insert_transactions
from security_utils import sanitize_input

st.set_page_config(page_title="Upload Transactions", page_icon="📤")
st.title("📤 Upload Your Transactions")

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
            st.error("❌ The uploaded file must contain the following columns: description, category, amount, date")
        else:
            df["category"] = df["category"].astype(str).str.strip().str.lower().apply(sanitize_input)
            df["description"] = df["description"].astype(str).apply(sanitize_input)

            # Clean and validate input
            df = df[df["category"].str.strip().astype(bool)]
            df = df[df["description"].str.strip().astype(bool)]

            # Limit length
            MAX_LENGTH = 100
            df["description"] = df["description"].str.slice(0, MAX_LENGTH)
            df["category"] = df["category"].str.slice(0, MAX_LENGTH)

            if df.empty:
                st.warning("🚫 No valid transactions to upload after cleaning.")
                st.stop()

            insert_transactions(df, email)
            st.success("✅ Transactions uploaded successfully!")

    except Exception as e:
        st.error(f"❌ Error uploading transactions: {e}")
