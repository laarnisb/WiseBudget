import streamlit as st
import pandas as pd
from database import get_user_by_email, insert_transaction

st.set_page_config(page_title="Upload Transactions", page_icon="📤")
st.title("📤 Upload Your Transactions")

st.markdown("""
Upload a CSV file with the following columns:

`date`, `description`, `category`, `amount`

**Accepted categories:** `Needs`, `Wants`, `Savings`
""")

# Ensure session has email
if "email" not in st.session_state:
    st.warning("⚠️ Please log in to upload transactions.")
    st.stop()

email = st.session_state["email"]
user = get_user_by_email(email)

if not user:
    st.error("User not found.")
    st.stop()

user_id = user["id"]

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Validate required columns
        required_cols = {"date", "description", "category", "amount"}
        if not required_cols.issubset(df.columns):
            st.error(f"CSV must contain columns: {', '.join(required_cols)}")
            st.stop()

        # Normalize category values
        valid_categories = ["Needs", "Wants", "Savings"]
        df["category"] = df["category"].str.capitalize()
        df = df[df["category"].isin(valid_categories)]

        if df.empty:
            st.warning("No valid transactions found after filtering by category.")
            st.stop()

        # Upload each transaction
        success_count = 0
        for _, row in df.iterrows():
            inserted = insert_transaction(
                user_id,
                str(row["date"]),
                row["description"],
                row["category"],
                float(row["amount"])
            )
            if inserted:
                success_count += 1

        st.success(f"✅ Successfully uploaded {success_count} transactions.")

    except Exception as e:
        st.error(f"❌ Failed to upload transactions: {e}")
