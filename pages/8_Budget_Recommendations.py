import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import get_engine

st.set_page_config(page_title="Budget Recommendations", page_icon="💡")
st.title("💡 Personalized Budget Recommendations")

# Ensure user is logged in
email = st.session_state.get("email", "")
if not email:
    st.warning("Please enter your email on the Home page.")
    st.stop()

try:
    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT t.category, SUM(t.amount) AS total
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE u.email = :email
            GROUP BY t.category
        """)
        result = conn.execute(query, {"email": email})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    if df.empty:
        st.info("ℹ️ No transactions found to generate recommendations.")
    else:
        # Define category groups
        needs = {"groceries", "rent", "utilities", "transportation", "insurance", "healthcare"}
        wants = {"dining", "entertainment", "shopping", "travel", "subscriptions"}
        savings = {"savings", "investments", "debt payment"}

        def assign_group(cat):
            cat = cat.strip().lower()
            if cat in needs:
                return "Needs"
            elif cat in wants:
                return "Wants"
            elif cat in savings:
                return "Savings"
            else:
                return "Other"

        df["group"] = df["category"].apply(assign_group)
        df = df[df["group"] != "Other"]

        group_summary = df.groupby("group")["total"].sum().reset_index()
        total_spent = group_summary["total"].sum()

        group_summary["actual"] = group_summary["total"] / total_spent
        group_summary["target"] = group_summary["group"].map({
            "Needs": 0.50,
            "Wants": 0.30,
            "Savings": 0.20
        })

        summary_df = group_summary[["group", "actual", "target"]]
        st.subheader("📊 Budget Allocation Summary")
        st.dataframe(summary_df.style.format({
            "actual": "{:.2%}",
            "target": "{:.2%}"
        }), use_container_width=True)

        # Generate Recommendations
        st.subheader("📝 Recommendations")
        recs = []

        for _, row in summary_df.iterrows():
            group = row["group"]
            actual = row["actual"]
            target = row["target"]

            # Safeguard against missing data
            if pd.isna(actual) or pd.isna(target):
                continue

            if group == "Needs" and actual > target * 1.1:
                recs.append("You're spending more than planned on Needs. Try identifying essential vs. non-essential items.")
            elif group == "Wants" and actual > target * 1.1:
                recs.append("Wants are exceeding budget. Consider limiting entertainment or luxury purchases.")
            elif group == "Savings" and actual < target * 0.9:
                recs.append("You're saving less than planned. Try setting up automatic transfers to savings.")
            elif group == "Needs" and actual < target * 0.9:
                recs.append("Great job keeping Needs below budget! Just ensure essential needs are met.")
            elif group == "Wants" and actual < target * 0.9:
                recs.append("You're well under on Wants. Consider allocating more to Savings if possible.")
            elif group == "Savings" and actual > target * 1.1:
                recs.append("Excellent! You're saving more than expected.")

        if recs:
            for r in recs:
                st.write(f"✅ {r}")
        else:
            st.success("🎯 Your spending is well-aligned with your budget goals!")

except Exception as e:
    st.error(f"❌ Error generating recommendations: {e}")
