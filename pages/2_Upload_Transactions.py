import streamlit as st
import pandas as pd
from database import insert_transactions

st.set_page_config(page_title="Upload Transactions", page_icon="📤")
st.title("📤 Upload Transactions")

# Ensure email is present in session state
email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page before uploading transactions.")
    st.stop()

# Upload section
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Basic validation
        required_cols = {"description", "category", "amount", "date"}
        if not required_cols.issubset(df.columns):
            st.error(f"❌ CSV must include columns: {', '.join(required_cols)}")
        else:
            # Add user email to each row
            df["user_email"] = email

            # Try inserting
            insert_transactions(df)
            st.success("✅ Transactions uploaded successfully!")

            # Preview
            st.subheader("Uploaded Data Preview")
            st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Failed to upload transactions: {e}")
