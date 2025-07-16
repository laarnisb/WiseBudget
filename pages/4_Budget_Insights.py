import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import get_transactions_by_user
from utils import get_user_id_by_email

st.set_page_config(page_title="💡 Budget Insights", page_icon="💡")
st.title("💡 Budget Insights")

st.markdown("### 📊 Monthly Spending by Category")

# Get user email from session state
email = st.session_state.get("email")

if not email:
    st.warning("⚠️ Please log in to view budget insights.")
else:
    user_id = get_user_id_by_email(email)
    if not user_id:
        st.error("User not found.")
    else:
        try:
            transactions = get_transactions_by_user(user_id)
            df = pd.DataFrame(transactions)

            if df.empty:
                st.info("No transactions found.")
            else:
                # Convert to datetime
                df["date"] = pd.to_datetime(df["date"])
                df["month"] = df["date"].dt.to_period("M").astype(str)

                # Exclude 'Income' from analysis
                df = df[df["category"] != "Income"]

                # Group by month and category
                monthly_summary = df.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0).reset_index()

                st.dataframe(monthly_summary, use_container_width=True)

                # Melt for plotting
                melted_df = pd.melt(monthly_summary, id_vars="month", var_name="category", value_name="amount")

                # Bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=melted_df, x="month", y="amount", hue="category", ax=ax)
                ax.set_title("Monthly Spending by Category (excluding Income)")
                ax.set_ylabel("Amount ($)")
                ax.set_xlabel("Month")
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Failed to fetch budget insights: {e}")
