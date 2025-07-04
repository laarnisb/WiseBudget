import streamlit as st
import pandas as pd
import plotly.express as px
import io
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="Budget Summary Reports", page_icon="📑")
st.title("📑 Budget Summary Reports")

email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

engine = get_engine()

try:
    with engine.connect() as conn:
        query = text("SELECT category, amount FROM transactions WHERE user_email = :email")
        df = pd.read_sql(query, conn, params={"email": email})

    if df.empty:
        st.info("No transactions found.")
    else:
        category_mapping = {
            "groceries": "Needs", "rent": "Needs", "utilities": "Needs", "transport": "Needs",
            "insurance": "Needs", "healthcare": "Needs", "internet": "Needs",
            "dining": "Wants", "entertainment": "Wants", "travel": "Wants", "shopping": "Wants",
            "subscriptions": "Wants",  "savings": "Savings", "investment": "Savings",
            "emergency fund": "Savings", "retirement": "Savings"
        }

        df["Group"] = df["category"].str.lower().map(category_mapping).fillna("Other")
        summary = df.groupby("Group")["amount"].sum().reset_index()
        summary.columns = ["Category Group", "Total Spending"]

        st.subheader("Spending Summary")
        st.dataframe(summary)

        fig = px.pie(summary, names="Category Group", values="Total Spending", title="Spending Distribution")
        st.plotly_chart(fig, use_container_width=True)

        # Export to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            summary.to_excel(writer, sheet_name="Summary", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Download Report as Excel",
            data=output,
            file_name="budget_summary_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

except Exception as e:
    st.error(f"❌ Error generating report: {e}")
