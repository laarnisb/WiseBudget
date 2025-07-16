import streamlit as st
import pandas as pd
from database import insert_transactions, get_user_id_by_email

st.set_page_config(page_title="📤 Upload Transactions", page_icon="📤")
st.title("📤 Upload Your Transactions")

# Sidebar greeting
if st.session_state.get("email"):
    st.sidebar.success(f"Welcome, {st.session_state.name}!")

# Require login
if not st.session_state.get("email"):
    st.warning("Please log in to upload transactions.")
    st.stop()

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
st.markdown("""
ℹ️ **Note:** Your CSV must contain these **case-sensitive** headers:
- `date`
- `description`
- `category`
- `amount`
""")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Validate headers
        required_cols = {"date", "description", "category", "amount"}
        if not required_cols.issubset(df.columns):
            st.error("CSV must have columns: date, description, category, amount.")
        else:
            # Get logged-in user's UUID
            user_id = get_user_id_by_email(st.session_state.email)
            if not user_id:
                st.error("❌ Could not retrieve user ID.")
            else:
                df["user_id"] = user_id
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

                # Only select allowed columns
                df = df[["user_id", "date", "description", "category", "amount"]]

                # Preview payload before upload
                payload = df.to_dict(orient="records")
                st.write("🔎 Payload preview:")
                st.json(payload)

                if not payload:
                    st.error("No valid transactions to upload.")
                else:
                    response = insert_transactions(payload)
                    if isinstance(response, dict) and "error" in response:
                        st.error(f"❌ Upload failed: {response['error']}")
                    else:
                        st.success("✅ Transactions uploaded successfully!")
                        st.dataframe(df)

    except Exception as e:
        st.error(f"Error processing file: {e}")
