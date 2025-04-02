import streamlit as st

from util import load_css

st.set_page_config(page_title="Healthy Blue", layout="centered")

load_css("styles/landing.css")


st.title("🌿 Welcome to Healthy Blue")

st.markdown(
    """
    ## Your Health Data, Transformed into Actionable Insights  

    Every step you take, every move you make, and every hour of activity—your health data holds a wealth of information about your well-being.  
    But raw numbers alone don’t tell the full story.  

    **Healthy Blue** bridges the gap between your personal health data and real-world factors like weather conditions.  
    We help you uncover patterns, optimize your routines, and make informed decisions for a healthier lifestyle.   

    **Your health data is more than just numbers—it's a story. Let Healthy Blue help you read it.**  
    """
)


if st.button("Click here to get started"):
    st.switch_page("pages/upload.py")
