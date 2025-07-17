import streamlit as st
import pandas as pd
from database import get_user_by_email, get_transactions_by_user, fetch_budget_goals_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="Budget Recommendations", page_icon="💡")
st.title("💡 Personalized Budget Recommendations")

if "email" not in st.session_state:
    st.warning("⚠️ Please log in to view your recommendations.")
    st.stop()

email = st.session_state.email
user_id = get_user_id_by_email(email)

# Fetch user's transactions and budget goals
transactions = get_transactions_by_user(user_id)
budget_goals = fetch_budget_goals_by_user(user_id)

if not transactions:
    st.warning("No transactions found. Please upload your spending data first.")
    st.stop()

if not budget_goals:
    st.warning("No budget goals found. Please set your goals first.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(transactions)
goals_df = pd.DataFrame(budget_goals)

# Filter only expenses
expenses_df = df[df['category'] != 'Income']
total_spent = expenses_df['amount'].sum()

# Calculate actual spending percentages by category
actual_percent = expenses_df.groupby("category")["amount"].sum() / total_spent * 100
actual_percent = actual_percent.reset_index().rename(columns={"amount": "actual"})

# Merge with goals
goals_df = goals_df.rename(columns={"budget_amount": "target", "category": "category"})
merged = pd.merge(goals_df, actual_percent, on="category", how="left").fillna(0)
merged["difference"] = merged["target"] - merged["actual"]

# Reorder columns: Target → Actual → Difference
summary_df = merged[["category", "target", "actual", "difference"]]
summary_df = summary_df.sort_values(by="category").reset_index(drop=True)

# Format as percentage for display
def format_percent(x):
    return f"{x:.2f}%"

styled_df = summary_df.copy()
styled_df[["target", "actual", "difference"]] = styled_df[["target", "actual", "difference"]].applymap(format_percent)

st.subheader("📊 Budget Allocation Summary")
st.dataframe(styled_df, hide_index=True)

# Generate Recommendations
st.subheader("📝 Recommendations")
for _, row in summary_df.iterrows():
    category = row["category"]
    diff = row["difference"]

    if diff < -5:
        st.error(f"⚠️ {category}: You're spending more than your target by {abs(diff):.2f}%. Consider reducing your expenses.")
    elif diff > 5:
        st.success(f"✅ {category}: You're under your target by {diff:.2f}%. Great job!")
    else:
        st.info(f"ℹ️ {category}: You're close to your target. Keep monitoring your spending.")
