# 💰 WiseBudget: A Personal Finance Recommendation System

**WiseBudget** is a secure, intelligent budgeting application designed to help individuals manage their finances using the 50/30/20 rule (Needs, Wants, Savings). Users can upload transactions, analyze their spending, set budget goals, track progress, get personalized recommendations, and forecast future spending—all within a privacy-focused environment.

---

## 📘 Project Background

Managing personal finances can be overwhelming, especially without tools that offer clarity and insight. **WiseBudget** was developed as a capstone project to empower users to:

- Make smarter financial decisions.
- Categorize transactions based on essential spending behaviors.
- Set and monitor monthly budget goals.
- Receive data-driven recommendations and forecasts.
- Interact with their data in a transparent, secure, and user-friendly platform.

The system combines secure data handling, predictive analytics, and visual insights to deliver a robust and personalized finance assistant.

---

## 🛠️ Approach to Implementation

WiseBudget integrates several modern tools and techniques to deliver a seamless budgeting experience:

### 🧩 Key Technologies

- **Streamlit** – Frontend interface for interacting with the budgeting system.
- **Supabase** – Backend service for authentication and secure data storage.
- **AES-256 Encryption** – Secures sensitive user data such as transaction records.
- **LSTM (Long Short-Term Memory)** – Predicts future spending patterns based on past behavior.
- **Modular Design** – Each page in the app performs a specific function (upload, insights, tracking, etc.).

### 🧱 Modules

- **User Registration/Login** – Authenticates users and creates private sessions.
- **Upload Transactions** – Accepts `.csv` files and stores encrypted data in Supabase.
- **View Budget Insights** – Automatically classifies transactions into Needs, Wants, Savings, and Others.
- **Set Budget Goals** – Lets users define their monthly financial targets.
- **Track Budget Progress** – Compares actual spending to goals using visual summaries.
- **Get Budget Recommendations** – Offers practical suggestions to improve financial habits.
- **Forecast Spending** – Uses an LSTM model to project future monthly spending.
- **Download Reports** – Generates budget summaries with charts for offline reference.

---

## 🚀 How to Run the App

### 🧰 Prerequisites

Install Python packages:

```bash
pip install -r requirements.txt
