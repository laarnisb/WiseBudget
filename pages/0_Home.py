import streamlit as st

# Set page configuration
st.set_page_config(page_title="🏠 Welcome to WiseBudget", page_icon="🏠")

# Sidebar greeting
if "email" in st.session_state and "name" in st.session_state:
    st.sidebar.success(f"👋 Welcome, {st.session_state['name']}!")
else:
    st.sidebar.info("🔐 Please log in to access all features.")

# Main content
st.title("🏠 Welcome to WiseBudget")
st.markdown("""
WiseBudget helps you take control of your personal finances by tracking expenses, setting budget goals, and generating insights using intelligent recommendations.
""")

# Display navigation options
st.subheader("🔎 What would you like to do today?")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/2_Upload_Transactions.py", label="⬆️ Upload Transactions", icon="📤")
    st.page_link("pages/3_View_Transactions.py", label="📄 View Transactions", icon="📋")

with col2:
    st.page_link("pages/4_Set_Budget_Goals.py", label="🎯 Set Budget Goals", icon="💰")
    st.page_link("pages/6_Track_Budget_Progress.py", label="📊 Track Budget Progress", icon="📈")

with col3:
    st.page_link("pages/7_Budget_Summary_Reports.py", label="🧾 View Summary Reports", icon="📑")
    st.page_link("pages/Logout.py", label="🚪 Logout", icon="🔒")

# Footer
st.markdown("---")
st.caption(f"📅 {datetime.now().strftime('%B %d, %Y')} — Logged in as: {st.session_state.get('email', 'Guest')}")
