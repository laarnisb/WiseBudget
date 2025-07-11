import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import text
from database import get_engine
from utils import get_current_user_email
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import datetime

st.set_page_config(page_title="Spending Forecast", page_icon="📈")
st.title("📈 Forecast Your Future Spending")

email = get_current_user_email()

if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

# Load model and setup
MODEL_PATH = "models/spending_forecast_lstm.h5"  # Make sure this exists
scaler = MinMaxScaler(feature_range=(0, 1))

try:
    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT t.date, t.amount
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE u.email = :email
            ORDER BY t.date ASC
        """)
        result = conn.execute(query, {"email": email})
        df = pd.DataFrame(result.fetchall(), columns=["date", "amount"])
        df["date"] = pd.to_datetime(df["date"])
except Exception as e:
    st.error(f"❌ Could not retrieve data: {e}")
    st.stop()

if df.empty:
    st.info("ℹ️ No transactions found to forecast.")
    st.stop()

# Prepare monthly total data
monthly = df.resample('M', on="date")["amount"].sum().reset_index()
monthly["date"] = pd.to_datetime(monthly["date"])
monthly.set_index("date", inplace=True)

# Scale data
scaled_data = scaler.fit_transform(monthly[["amount"]])
window_size = 3

X = []
for i in range(window_size, len(scaled_data)):
    X.append(scaled_data[i-window_size:i, 0])

X = np.array(X)
X = X.reshape((X.shape[0], X.shape[1], 1))

# Load pre-trained model
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    st.error(f"❌ LSTM model not found: {e}")
    st.stop()

# Predict next month's spending
last_sequence = scaled_data[-window_size:].reshape(1, window_size, 1)
predicted_scaled = model.predict(last_sequence)
predicted_amount = scaler.inverse_transform(predicted_scaled)[0][0]

# Plot forecast
st.subheader("📊 Monthly Spending Forecast")
plt.figure(figsize=(10, 4))
plt.plot(monthly.index, monthly["amount"], label="Historical")
future_date = monthly.index[-1] + pd.DateOffset(months=1)
plt.axvline(future_date, color='gray', linestyle='--')
plt.scatter(future_date, predicted_amount, color='red', label="Forecast")
plt.title("Forecast for Next Month's Spending")
plt.xlabel("Month")
plt.ylabel("Amount ($)")
plt.legend()
st.pyplot(plt)

# Insight message
st.subheader("🧠 Forecast Insight")
st.markdown(f"""
Based on your past {window_size} months of spending, you're forecasted to spend approximately  
**${predicted_amount:,.2f}** next month.

> This projection can help you plan ahead and adjust your budget accordingly.
""")
