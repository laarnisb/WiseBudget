import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine
import plotly.graph_objects as go

st.set_page_config(page_title="Track Budget Progress", page_icon="📈")
st.title("📈 Track Budget Progress")

email = st.session_state.get("email", "")

if email:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            user_query = text("SELECT id FROM users WHERE email = :email")
            user_result = conn.execute(user_query, {"email": email}).fetchone()

            if user_result:
                user_id = user_result[0]

                goals_query = text("""
                    SELECT income, needs_percent, wants_percent, savings_percent
                    FROM budget_goals WHERE user_id = :user_id
                """)
                goals_result = conn.execute(goals_query, {"user_id": user_id}).fetchone()

                if goals_result:
                    income, needs_pct, wants_pct, savings_pct = goals_result
                    budget = {
                        "Needs": round(income * needs_pct / 100, 2),
                        "Wants": round(income * wants_pct / 100, 2),
                        "Savings": round(income * savings_pct / 100, 2)
                    }

                    txn_query = text("SELECT category, amount FROM transactions WHERE user_id = :user_id")
                    txn_result = conn.execute(txn_query, {"user_id": user_id})
                    txn_df = pd.DataFrame(txn_result.fetchall(), columns=["category", "amount"])

                    if not txn_df.empty:
                        category_mapping = {
                            "groceries": "Needs", "rent": "Needs", "utilities": "Needs", "transport": "Needs",
                            "insurance": "Needs", "healthcare": "Needs", "internet": "Needs",
                            "dining": "Wants", "entertainment": "Wants", "travel": "Wants", "shopping": "Wants",
                            "subscriptions": "Wants", "savings": "Savings", "investment": "Savings",
                            "emergency fund": "Savings", "retirement": "Savings"
                        }
                        txn_df["group"] = txn_df["category"].map(category_mapping).fillna("Other")
                        actual = txn_df.groupby("group")["amount"].sum().to_dict()

                        for key in ["Needs", "Wants", "Savings"]:
                            actual.setdefault(key, 0)

                        comparison_df = pd.DataFrame({
                            "Budgeted": pd.Series(budget),
                            "Actual": pd.Series(actual)
                        })
                        comparison_df["Difference"] = comparison_df["Actual"] - comparison_df["Budgeted"]
                        st.subheader("📊 Budget vs. Actual Spending")
                        st.dataframe(comparison_df)

                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=list(budget.keys()), y=list(budget.values()), name="Budgeted"))
                        fig.add_trace(go.Bar(x=list(actual.keys()), y=list(actual.values()), name="Actual"))
                        fig.update_layout(barmode='group', title="Budget Comparison", yaxis_title="Amount ($)")
                        st.plotly_chart(fig)

                    else:
                        st.info("ℹ️ No transactions found.")
                else:
                    st.warning("⚠️ No budget goals found for this user.")
            else:
                st.warning("⚠️ User not found.")
    except Exception as e:
        st.error(f"❌ Error loading budget progress: {e}")
else:
    st.info("Please enter your email on the Home page to proceed.")
