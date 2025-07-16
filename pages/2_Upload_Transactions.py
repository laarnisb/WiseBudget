import streamlit as st
import pandas as pd
from database import insert_transactions, get_user_by_email

st.set_page_config(page_title="Upload Transactions", page_icon="📤")
st.title("📤 Upload Your Transactions")

# Ensure the user is logged in
if "email" not in st.session_state or not st.session_state.email:
    st.warning("Please log in to upload transactions.")
    st.stop()

st.info("ℹ️ **Note**: Your CSV file must contain the following column headers:")
st.markdown("""
- `date`  
- `description`  
- `category`  
- `amount`  
\n
These headers are **case-sensitive** and must be spelled exactly.
""")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        expected_columns = {"date", "description", "category", "amount"}
        if not expected_columns.issubset(df.columns):
            st.error(f"❌ Missing required columns. Found: {list(df.columns)}")
            st.stop()

        # Normalize category values
        df["category"] = df["category"].str.strip().str.capitalize()

        # Get user ID
        user = get_user_by_email(st.session_state.email)
        if not user or "id" not in user:
            st.error("❌ User not found or data error.")
            st.stop()

        user_id = user["id"]
        df["user_id"] = user_id
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Filter valid rows only
        df = df.dropna(subset=["date", "description", "category", "amount"])

        payload = df[["user_id", "date", "description", "category", "amount"]].to_dict(orient="records")

        if not payload:
            st.error("No valid transactions to upload.")
        else:
            response = insert_transactions(payload)
            if isinstance(response, dict) and "error" in response:
                st.error(f"❌ Upload failed: {response['error']}")
            else:
                st.success("✅ Transactions uploaded successfully!")
                st.dataframe(df[["user_id", "date", "description", "category", "amount"]])
    except Exception as e:
        st.error(f"❌ Failed to upload transactions: {str(e)}")
