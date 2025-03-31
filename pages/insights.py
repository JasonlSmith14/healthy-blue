import random
import pandas as pd
import streamlit as st
from streamlit_pills import pills
from PIL import Image

from config import database
from insights.formatting import ResponseFormatter
from insights.insights import Insights
from models.insight_data import InsightData


st.set_page_config(layout="wide", page_title="Your Insights")


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles.css")

day_with_most_steps_tab = "Your most active day 🏆"
day_with_greatest_distance_tab = "The longest distance you traveled in a day 🚶‍♂️🌍"
month_with_most_steps_tab = "Your busiest month on foot 📅✨"

day_with_least_steps_tab = "Your most restful day 😌"
day_with_smallest_distance_tab = "Shortest distance traveled in a day 🛋️"
month_with_least_steps_tab = "Your most relaxed month 📆💤"

hottest_day_tab = "The hottest day you powered through 🔥🌞"
coldest_day_tab = "The chilliest day you faced ❄️🧤"

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

steps_by_year_insight_data = InsightData(
    dataframe=steps_by_year, date_column="year", date_format="%Y"
)
steps_by_month_insight_data = InsightData(
    dataframe=steps_by_month, date_column="month_of_the_year", date_format="%Y-%m"
)
steps_by_day_insight_data = InsightData(
    dataframe=steps_by_day, date_column="recorded_date", date_format="%Y-%m-%d"
)

insights = Insights(
    steps_by_year=steps_by_year_insight_data,
    steps_by_month=steps_by_month_insight_data,
    steps_by_day=steps_by_day_insight_data,
)


if "shuffled_list" not in st.session_state:
    insights_list = [
        (day_with_most_steps_tab, insights.day_with_most_steps),
        (day_with_greatest_distance_tab, insights.day_with_greatest_distance),
        (month_with_most_steps_tab, insights.month_with_most_steps),
        (day_with_least_steps_tab, insights.day_with_least_steps),
        (day_with_smallest_distance_tab, insights.day_with_smallest_distance),
        (month_with_least_steps_tab, insights.month_with_least_steps),
        (hottest_day_tab, insights.hottest_day),
        (coldest_day_tab, insights.coldest_day),
    ]
    random.shuffle(insights_list)
    st.session_state["shuffled_list"] = insights_list
else:
    insights_list = st.session_state["shuffled_list"]

insight_names = [tab for tab, _ in insights_list]
insights_map = {tab: fn for tab, fn in insights_list}

with st.sidebar:
    selected_insight = pills("Available Insights: ", insight_names, index=None)

    years = insights.years_available()
    year_option = pills(
        f"Are you interested in seeing a year other than {max(years)}?",
        options=[year for year in years[::-1]],
    )


def display_insight(selected_insight: str):
    insight_pkaceholder = st.empty()
    previous_placeholder = st.empty()
    title_placeholder = st.empty()
    highlight_placeholder = st.empty()
    fun_placeholder = st.empty()
    challenge_placeholder = st.empty()

    insight_function = insights_map[selected_insight]

    insight_pkaceholder.markdown(f"# {selected_insight}")
    with st.spinner("Generating insight...", show_time=True):
        if selected_insight in st.session_state:
            insight: ResponseFormatter = st.session_state[selected_insight]
            previous_placeholder.info("This insight was previously determined")
        else:
            insight = insight_function()
            st.session_state[selected_insight] = insight

    title_placeholder.header(insight.title)
    highlight_placeholder.subheader(insight.highlight)
    fun_placeholder.write(insight.fun_to_know)
    challenge_placeholder.write(insight.challenge)


if selected_insight:
    display_insight(selected_insight=selected_insight)

# Look more at data behind your insights - expander with more raw data
# Classify chain as good/bad - question why it was bad: Becomes interactive; provide suggestion on how to improve
# Styling
# Authentication since it is health data
# Done is better than perfect
# Dribble: Triad mix of colours
