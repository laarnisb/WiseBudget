import streamlit as st

st.set_page_config(page_title="WiseBudget Home", page_icon="🏠")
st.title("🏠 Welcome to WiseBudget")

st.markdown("""
WiseBudget is your personal finance dashboard designed to help you:

📤 Upload and track your expenses  
🎯 Set budget goals using the 50/30/20 rule  
📊 Monitor your budget progress  
📋 View detailed insights and summary reports  
💡 Receive personalized spending recommendations  
📈 Forecast your future spending patterns  
""")

st.markdown("""
To get started, click on **Login/Register** in the sidebar.  
Once you're logged in, you'll unlock all the excellent features of WiseBudget, personalized just for you!
""")

# Optional horizontal rule
st.markdown("---")

# Trust notice
st.markdown("🔒 **Your data is private and encrypted.**")
