import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database import insert_transactions

st.set_page_config(page_title="Upload Transactions", page_icon="📤")

st.title("📤 Upload Transactions")

st.markdown("Upload your transactions as a CSV file. Required columns: `description`, `amount`, `date`, and `user_email`. Optional: `category`.")

# Define the smart categorization function
def categorize_transaction(description):
    description = description.lower()

    category_keywords = {
        "Groceries": ["grocery", "supermarket", "walmart", "aldi", "trader joe", "whole foods"],
        "Rent": ["rent", "landlord", "apartment"],
        "Utilities": ["electric", "water", "gas", "utility", "internet", "wifi"],
        "Transportation": ["uber", "lyft", "gas", "fuel", "transit", "train", "bus"],
        "Dining": ["restaurant", "cafe", "mcdonald", "burger", "coffee", "starbucks"],
        "Entertainment": ["netflix", "spotify", "cinema", "movie", "concert"],
        "Healthcare": ["pharmacy", "doctor", "hospital", "clinic"],
        "Shopping": ["amazon", "shopping", "store", "target", "costco"],
        "Savings": ["transfer", "savings", "deposit"]
    }

    for category, keywords in category_keywords.items():
        if any(keyword in description for keyword in keywords):
            return category

    return "Uncategorized"

# CSV Upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Validate required columns
        required_columns = ["description", "amount", "date", "user_email"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ Missing required columns. Please include: {', '.join(required_columns)}")
        else:
            # Auto-categorize if missing or blank
            if "category" not in df.columns:
                df["category"] = df["description"].apply(categorize_transaction)
            else:
                df["category"] = df.apply(
                    lambda row: row["category"] if pd.notna(row["category"]) and row["category"].strip() != "" else categorize_transaction(row["description"]),
                    axis=1
                )

            # Convert date to proper format
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            if df["date"].isnull().any():
                st.error("❌ One or more dates could not be parsed. Please ensure all dates are in a valid format (e.g., YYYY-MM-DD).")
            else:
                insert_transactions(df)
                st.success("✅ Transactions uploaded successfully!")
                st.dataframe(df)

    except SQLAlchemyError as e:
        st.error(f"❌ Database error: {e}")
    except Exception as e:
        st.error(f"❌ Error: {e}")
