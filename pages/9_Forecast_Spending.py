import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="Forecast Spending", page_icon="📈")
st.title("📈 Spending Forecast")

# --- Ensure email exists in session ---
email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

# --- Load transactions ---
engine = get_engine()
with engine.connect() as conn:
    result = conn.execute(
        text("""
            SELECT t.date, t.amount
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE u.email = :email
            ORDER BY t.date
        """),
        {"email": email}
    )
    df = pd.DataFrame(result.fetchall(), columns=["date", "amount"])

if df.empty:
    st.info("ℹ️ No transactions found for this user.")
    st.stop()

# --- Preprocess ---
df["date"] = pd.to_datetime(df["date"])
monthly = df.resample("M", on="date")["amount"].sum().reset_index()

if len(monthly) < 3:
    st.warning("❌ Not enough data to generate a forecast. At least 3 months required.")
    st.stop()

# --- Scale + Prepare Input ---
scaler = MinMaxScaler()
scaled = scaler.fit_transform(monthly[["amount"]])

WINDOW_SIZE = 3
input_sequence = scaled[-WINDOW_SIZE:]
X_input = input_sequence.reshape((1, WINDOW_SIZE, 1))

# --- Load Model + Predict ---
model = load_model("models/spending_forecast_lstm.h5", compile=False)
predicted_scaled = model.predict(X_input)
predicted_amount = scaler.inverse_transform(predicted_scaled)[0][0]

# --- Display Forecast ---
next_month = monthly["date"].max() + pd.DateOffset(months=1)
forecast_df = monthly.copy()
forecast_df = pd.concat([forecast_df, pd.DataFrame([{"date": next_month, "amount": predicted_amount}])], ignore_index=True)

st.subheader("📊 Monthly Spending with Forecast")
st.line_chart(forecast_df.set_index("date")["amount"])

st.success(f"🔮 Forecasted spending for {next_month.strftime('%B %Y')}: **${predicted_amount:.2f}**")
