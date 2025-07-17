import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_user_by_email, get_transactions_by_user, fetch_budget_goals_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="📊 Track Budget Progress", page_icon="📊")
st.title("📊 Track Budget Progress")

# Get email from session state
if "email" not in st.session_state:
    st.warning("⚠️ Please log in to view your budget progress.")
    st.stop()

email = st.session_state["email"]
user_id = get_user_id_by_email(email)

# Fetch transactions
transactions = get_transactions_by_user(user_id)
if not transactions:
    st.warning("No transactions found.")
    st.stop()

df = pd.DataFrame(transactions)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period("M").astype(str)

# Select month
available_months = sorted(df['month'].unique())
selected_month = st.selectbox("Select a month", available_months)

# Filter transactions
monthly_df = df[df['month'] == selected_month]

# Load goals
budget_goals = fetch_budget_goals_by_user(user_id)
if not budget_goals:
    st.warning("No budget goals set yet. Please set goals first.")
    st.stop()

goals_df = pd.DataFrame(budget_goals)

# Calculate income for the month
monthly_income = monthly_df[monthly_df['category'] == 'Income']['amount'].sum()

# Calculate target budgets
goals_df['budgeted'] = goals_df['budget_amount'] / 100 * monthly_income

# Calculate actual spending
actuals = monthly_df.groupby('category')['amount'].sum().reset_index()
actuals.columns = ['category', 'actual']

# Merge goals with actuals
summary_df = goals_df.merge(actuals, left_on='category', right_on='category', how='left')
summary_df['actual'] = summary_df['actual'].fillna(0)

# Calculate difference: target - actual
summary_df['difference'] = summary_df['budgeted'] - summary_df['actual']
summary_df['budgeted'] = summary_df['budgeted'].round(2)
summary_df['actual'] = summary_df['actual'].round(2)
summary_df['difference'] = summary_df['difference'].round(2)

# Display summary
st.subheader(f"Summary for {selected_month}")
st.dataframe(summary_df[['category', 'budgeted', 'actual', 'difference']].rename(columns={
    'category': 'Category',
    'budgeted': 'Budgeted',
    'actual': 'Actual',
    'difference': 'Difference'
}), use_container_width=True)

# Bar chart
st.subheader("Budgeted vs Actual Spending")
fig, ax = plt.subplots()

categories = summary_df['category']
budgeted = summary_df['budgeted']
actual = summary_df['actual']
difference = summary_df['difference']

bar_width = 0.35
x = range(len(categories))

ax.bar(x, budgeted, width=bar_width, label='Budgeted')
ax.bar([i + bar_width for i in x], actual, width=bar_width, label='Actual')

# Annotate bars with difference
for i, (b, a, d) in enumerate(zip(budgeted, actual, difference)):
    color = 'green' if d >= 0 else 'red'
    ax.text(i + bar_width, max(b, a) + 10, f"${d:.2f}", ha='center', color=color, fontsize=10)

ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(categories)
ax.set_ylabel("Amount ($)")
ax.set_title("Budgeted vs Actual Spending")
ax.legend()

st.pyplot(fig)
