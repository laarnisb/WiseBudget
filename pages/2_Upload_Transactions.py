import streamlit as st
import pandas as pd
import datetime
from database import insert_transactions
from auth import get_logged_in_user_email

st.title("📤 Upload Transactions")

st.markdown("Upload a CSV file with the columns: `description`, `amount`, `date`.")
st.markdown("The system will automatically categorize transactions into **Needs**, **Wants**, or **Savings**.")

# Auto-categorize function
def auto_categorize(description):
    desc = description.lower()
    if any(keyword in desc for keyword in ["grocery", "rent", "utilities", "mortgage", "insurance", "medical", "gas", "electric", "water", "internet"]):
        return "Needs"
    elif any(keyword in desc for keyword in ["netflix", "dining", "shopping", "entertainment", "uber", "lyft", "vacation", "movie"]):
        return "Wants"
    elif any(keyword in desc for keyword in ["transfer", "investment", "savings", "deposit", "retirement", "401k", "roth"]):
        return "Savings"
    else:
        return "Other"

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Validate required columns
        required_cols = {"description", "amount", "date"}
        if not required_cols.issubset(set(df.columns)):
            st.error(f"❌ Missing required columns: {required_cols - set(df.columns)}")
        else:
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df["category"] = df["description"].apply(auto_categorize)
            df["user_email"] = get_logged_in_user_email()

            # Drop invalid rows
            df.dropna(subset=["amount", "date"], inplace=True)

            if df.empty:
                st.warning("⚠️ No valid transactions found after cleaning.")
            else:
                insert_transactions(df)
                st.success("✅ Transactions uploaded and categorized successfully!")
                st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Failed to process file: {str(e)}")
