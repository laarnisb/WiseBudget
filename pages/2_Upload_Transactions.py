import streamlit as st
import pandas as pd
from database import insert_transactions, get_user_by_email

st.set_page_config(page_title="📤 Upload Transactions", page_icon="📤")
st.title("📤 Upload Your Transactions")

# Display sidebar message if logged in
if st.session_state.email:
    st.sidebar.success(f"Welcome, {st.session_state.name}!")

# Only allow access if logged in
if not st.session_state.get("email"):
    st.warning("Please log in to upload transactions.")
    st.stop()

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
st.markdown("""
ℹ️ **Note:** Your CSV file must contain the following column headers:
- `date`
- `description`
- `category`
- `amount`

These headers are **case-sensitive** and must be spelled exactly.
""")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = {"date", "description", "amount", "category"}
        if not required_columns.issubset(df.columns):
            st.error("CSV must contain columns: date, description, amount, category.")
        else:
            user_email = st.session_state.email
            user_id = get_user_by_email(user_email)

            if user_id:
                df["user_id"] = user_id
                response = insert_transactions(df.to_dict(orient="records"))
                if "error" in response:
                    st.error(f"❌ Failed to upload transactions: {response['error']}")
                else:
                    st.success("✅ Transactions uploaded successfully!")
                    st.dataframe(df)
            else:
                st.error("❌ Failed to retrieve user ID.")
            
    except Exception as e:
        st.error(f"Error processing file: {e}")
