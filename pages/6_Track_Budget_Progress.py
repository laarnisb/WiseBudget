import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine
import plotly.graph_objects as go

st.set_page_config(page_title="Track Budget Progress", page_icon="📈")
st.title("📈 Track Budget Progress")

email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

engine = get_engine()

try:
    with engine.connect() as conn:
        user_result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email}).fetchone()

        if not user_result:
            st.warning("User not found.")
        else:
            user_id = user_result[0]

            goals_query = text("SELECT income, needs_percent, wants_percent, savings_percent FROM budget_goals WHERE user_id = :user_id")
            goals = conn.execute(goals_query, {"user_id": user_id}).fetchone()

            if not goals:
                st.warning("No budget goals set.")
            else:
                income, needs_pct, wants_pct, savings_pct = goals
                budget = {
                    "Needs": income * needs_pct / 100,
                    "Wants": income * wants_pct / 100,
                    "Savings": income * savings_pct / 100
                }

                txn_query = text("SELECT category, amount FROM transactions WHERE user_email = :email")
                txn_df = pd.read_sql(txn_query, conn, params={"email": email})

                category_mapping = {
                    "groceries": "Needs", "rent": "Needs", "utilities": "Needs", "transport": "Needs",
                    "insurance": "Needs", "healthcare": "Needs", "internet": "Needs",
                    "dining": "Wants", "entertainment": "Wants", "travel": "Wants", "shopping": "Wants",
                    "subscriptions": "Wants",  "savings": "Savings", "investment": "Savings",
                    "emergency fund": "Savings", "retirement": "Savings"
                }

                txn_df["group"] = txn_df["category"].str.lower().map(category_mapping).fillna("Other")
                actual = txn_df.groupby("group")["amount"].sum().to_dict()

                for key in ["Needs", "Wants", "Savings"]:
                    actual.setdefault(key, 0)

                comparison_df = pd.DataFrame({
                    "Budgeted": pd.Series(budget),
                    "Actual": pd.Series(actual)
                })
                comparison_df["Difference"] = comparison_df["Actual"] - comparison_df["Budgeted"]

                st.subheader("💰 Budget vs. Actual")
                st.dataframe(comparison_df)

                fig = go.Figure()
                fig.add_trace(go.Bar(x=comparison_df.index, y=comparison_df["Budgeted"], name="Budgeted"))
                fig.add_trace(go.Bar(x=comparison_df.index, y=comparison_df["Actual"], name="Actual"))
                fig.update_layout(barmode="group", title="Spending Comparison", yaxis_title="Amount ($)")
                st.plotly_chart(fig)

except Exception as e:
    st.error(f"❌ Error tracking progress: {e}")
