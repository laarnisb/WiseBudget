import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from database import get_transactions_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="Forecast Spending", page_icon="📈")
st.title("📈 Spending Forecast")

# --- Ensure email exists in session ---
if "email" not in st.session_state:
    st.warning("⚠️ Please log in to view this page.")
    st.stop()

email = st.session_state["email"]
user_id = get_user_id_by_email(email)

# --- Load transactions from Supabase ---
transactions = get_transactions_by_user(user_id)
if not transactions:
    st.info("ℹ️ No transactions found for this user.")
    st.stop()

# --- Convert to DataFrame ---
df = pd.DataFrame(transactions)
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df.dropna(subset=["amount", "date"], inplace=True)

# --- Monthly aggregation ---
monthly = df.resample("M", on="date")["amount"].sum().reset_index()

if len(monthly) < 3:
    st.warning("❌ Not enough data to generate a forecast. At least 3 months required.")
    st.stop()

# --- Scaling and Input Preparation ---
scaler = MinMaxScaler()
scaled = scaler.fit_transform(monthly[["amount"]])

WINDOW_SIZE = 3
input_sequence = scaled[-WINDOW_SIZE:]
X_input = input_sequence.reshape((1, WINDOW_SIZE, 1))

# --- Load Model and Predict ---
model = load_model("models/spending_forecast_lstm.h5", compile=False)
predicted_scaled = model.predict(X_input)
predicted_amount = scaler.inverse_transform(predicted_scaled)[0][0]

# --- Add Prediction to Forecast Table ---
next_month = monthly["date"].max() + pd.DateOffset(months=1)
forecast_df = pd.concat([
    monthly,
    pd.DataFrame([{"date": next_month, "amount": predicted_amount}])
], ignore_index=True)

# --- Display ---
st.subheader("Monthly Spending with Forecast")
st.line_chart(forecast_df.set_index("date")["amount"])

st.success(f"🔮 Forecasted spending for {next_month.strftime('%B %Y')}: **${predicted_amount:.2f}**")
