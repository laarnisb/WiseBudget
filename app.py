import streamlit as st

st.set_page_config(page_title="WiseBudget Home", page_icon="🏠")
st.title("🏠 Welcome to WiseBudget")

st.markdown("""
WiseBudget is your personal finance dashboard designed to help you:

📤 Upload and track your expenses  
🎯 Set budget goals using the 50/30/20 rule  
📈 Monitor your budget progress  
📑 View detailed insights and summary reports  
💡 Receive personalized spending recommendations  
📊 Forecast your future spending patterns  
""")

st.markdown("""
To get started, choose **Login/Register** from the sidebar.  
Once logged in, you’ll have access to all WiseBudget features personalized to your account.
""")

# Optional horizontal rule
st.markdown("---")

# Trust notice
st.markdown("🔒 **Your data is private and encrypted.**")