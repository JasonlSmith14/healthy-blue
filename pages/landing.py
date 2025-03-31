import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Health Data Insights", page_icon=":guardsman:", layout="wide"
)

st.markdown(
    """
    <style>
        body {
            background-image: url('https://raw.githubusercontent.com/JasonlSmith14/healthy-blue/main/static/landing.webp');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;  /* Full screen height */
            color: #ffffff;  /* White text color for contrast */
        }
        .stApp {
            background: rgba(255, 255, 255, 0.8);  /* Optional: slightly transparent background for app content */
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Title and description
st.title("Welcome to the Health Data Insights App")
st.markdown(
    """
    This app allows you to upload your health data, analyze it, and get insights on various health metrics such as steps, calories, and heart rate.
    
    Simply upload your health data file in CSV format, and we'll process it to give you detailed insights on your health patterns.
    """
)

if st.button("Click here to get started viewing your health insights"):
    st.switch_page("pages/insights.py")
