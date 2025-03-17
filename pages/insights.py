import pandas as pd
from config import database
import streamlit as st
from insights.insights import Insights

st.set_page_config(layout="wide")
st.sidebar.page_link("main.py", label="Upload Your Data")
st.sidebar.page_link("pages/insights.py", label="Your Insights")

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

(
    day_with_most_steps_tab,
    month_with_most_steps_tab,
    steps_over_the_year_tab,
    average_max_min_steps_by_month_tab,
    distance_over_the_year_tab,
    average_max_min_distance_by_month_tab,
    steps_over_the_years_tab,
) = st.tabs(
    [
        "Your day with most steps",
        "Your month with most steps",
        "Your steps over the year",
        "Your average and maximum steps over the year",
        "Your distances over the year",
        "Your average and maximum distances over the year",
        "Your steps over the years",
    ]
)

with day_with_most_steps_tab:
    insights.day_with_most_steps()

with month_with_most_steps_tab:
    insights.month_with_most_steps()

with steps_over_the_year_tab:
    insights.steps_over_the_year()

with steps_over_the_years_tab:
    insights.steps_over_the_years()

with average_max_min_steps_by_month_tab:
    insights.average_max_min_steps_by_month()

with distance_over_the_year_tab:
    insights.distance_over_the_year()

with average_max_min_distance_by_month_tab:
    insights.average_max_min_distance_by_month()
