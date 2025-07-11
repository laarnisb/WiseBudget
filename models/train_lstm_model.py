import os
import pandas as pd
import numpy as np
from sqlalchemy import text
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from database import get_engine

# --- Load Data ---
engine = get_engine()
with engine.connect() as conn:
    result = conn.execute(text("SELECT date, amount FROM transactions"))
    df = pd.DataFrame(result.fetchall(), columns=["date", "amount"])

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# --- Aggregate Monthly ---
monthly = df.resample("M", on="date")["amount"].sum().reset_index()
print("📅 Number of monthly records available:", len(monthly))

# --- Scale Data ---
scaler = MinMaxScaler()
scaled = scaler.fit_transform(monthly[["amount"]])

# --- Prepare Sequences ---
WINDOW_SIZE = 3
X, y = [], []

if len(scaled) <= WINDOW_SIZE:
    raise ValueError("❌ Not enough data points to train the LSTM model. Add more monthly transaction data.")

for i in range(WINDOW_SIZE, len(scaled)):
    X.append(scaled[i-WINDOW_SIZE:i, 0])
    y.append(scaled[i, 0])

X = np.array(X)
y = np.array(y)
X = X.reshape((X.shape[0], X.shape[1], 1))

# --- Build LSTM Model ---
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(WINDOW_SIZE, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# --- Train Model ---
model.fit(X, y, epochs=75, verbose=1)

# --- Save Model ---
output_dir = "models"
os.makedirs(output_dir, exist_ok=True)
model.save(os.path.join(output_dir, "spending_forecast_lstm.h5"))
print("✅ Model trained and saved to models/spending_forecast_lstm.h5")
