import pandas as pd
from config import database
import streamlit as st
from insights.insights import Insights

st.set_page_config(layout="wide")
st.sidebar.page_link("main.py", label="Upload Your Data")
st.sidebar.page_link("pages/insights.py", label="Your Insights")

day_with_most_steps_tab = "Your most active day 🏆"
day_with_greatest_distance_tab = "The longest distance you traveled in a day 🚶‍♂️🌍"
month_with_most_steps_tab = "Your busiest month on foot 📅✨"

day_with_least_steps_tab = "Your most restful day 😌"
day_with_smallest_distance_tab = "Shortest distance traveled in a day 🛋️"
month_with_least_steps_tab = "Your most relaxed month 📆💤"

hottest_day_tab = "The hottest day you powered through 🔥🌞"
coldest_day_tab = "The chilliest day you faced ❄️🧤"

year_overview_tab = "Your year in motion! 🎉🚀"

tab_selection = st.sidebar.selectbox(
    "Which insight would you like to see?",
    [
        "Please select an option",
        day_with_most_steps_tab,
        day_with_greatest_distance_tab,
        month_with_most_steps_tab,
        day_with_least_steps_tab,
        day_with_smallest_distance_tab,
        month_with_least_steps_tab,
        hottest_day_tab,
        coldest_day_tab,
        year_overview_tab,
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

insights_map = {
    day_with_most_steps_tab: insights.day_with_most_steps,
    day_with_greatest_distance_tab: insights.day_with_greatest_distance,
    month_with_most_steps_tab: insights.month_with_most_steps,
    hottest_day_tab: insights.hottest_day,
    coldest_day_tab: insights.coldest_day,
    day_with_least_steps_tab: insights.day_with_least_steps,
    day_with_smallest_distance_tab: insights.day_with_smallest_distance,
    month_with_least_steps_tab: insights.month_with_least_steps,
    year_overview_tab: insights.overview_of_years,
}

insights_map.get(tab_selection, lambda: None)()
