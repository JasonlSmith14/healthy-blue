import pandas as pd
from config import database
import streamlit as st
from insights.insights import Insights

st.set_page_config(layout="wide")
st.sidebar.page_link("main.py", label="Upload Your Data")
st.sidebar.page_link("pages/insights.py", label="Your Insights")

day_with_most_steps_tab = "Day with the most steps"
day_with_greatest_distance_tab = "Day with the greatest distance traveled"
month_with_most_steps_tab = "Month with the most steps"

tab_selection = st.sidebar.selectbox(
    "Which insight would you like to see?",
    [
        "Please select an option",
        "Day with the most steps",
        "Day with the greatest distance traveled",
        "Month with the most steps",
    ],
)

steps_by_year_tag = "steps_by_year"
steps_by_month_tag = "steps_by_month"
steps_by_day_tag = "steps_by_day"

if steps_by_year_tag not in st.session_state:
    steps_by_year = pd.read_sql("SELECT * FROM gold_steps_by_year", database.engine)
    st.session_state[steps_by_year_tag] = steps_by_year

if steps_by_month_tag not in st.session_state:
    steps_by_month = pd.read_sql("SELECT * FROM gold_steps_by_month", database.engine)
    st.session_state[steps_by_month_tag] = steps_by_month

if steps_by_day_tag not in st.session_state:
    steps_by_day = pd.read_sql("SELECT * FROM gold_steps_by_day", database.engine)
    st.session_state[steps_by_day_tag] = steps_by_day


steps_by_year: pd.DataFrame = st.session_state[steps_by_year_tag]
steps_by_month: pd.DataFrame = st.session_state[steps_by_month_tag]
steps_by_day: pd.DataFrame = st.session_state[steps_by_day_tag]

insights = Insights(
    steps_by_year=steps_by_year,
    steps_by_month=steps_by_month,
    steps_by_day=steps_by_day,
)

insights.years_available()

if tab_selection == day_with_most_steps_tab:
    insights.day_with_most_steps()

if tab_selection == day_with_greatest_distance_tab:
    insights.day_with_greatest_distance()

if tab_selection == month_with_most_steps_tab:
    insights.month_with_most_steps()
    
