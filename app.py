import streamlit as st

# Set page configuration
st.set_page_config(page_title="Healthy Blue", layout="centered")


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/landing.css")


st.title("🌿 Welcome to Healthy Blue")
st.markdown(
    """
    **Healthy Blue** helps you analyze your health data and understand how the weather affects your activities.  
    Simply upload your health data, and we'll generate insights tailored to you.  
    """
)

if st.button("Click here to get started viewing your health insights"):
    st.switch_page("pages/upload.py")
