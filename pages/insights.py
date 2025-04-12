import pandas as pd
import streamlit as st
from streamlit_pills import pills

from config import database
from insights.formatting import InsightsFormatter
from insights.insights import Insights
from models.insight_data import InsightData
from util import load_css


st.set_page_config(layout="wide", page_title="Your Insights")

load_css("styles/insights.css")

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

years = steps_by_year_insight_data.years_available()

insight_names = [
    day_with_most_steps_tab,
    day_with_greatest_distance_tab,
    month_with_most_steps_tab,
    day_with_least_steps_tab,
    day_with_smallest_distance_tab,
    month_with_least_steps_tab,
    hottest_day_tab,
    coldest_day_tab,
]

with st.sidebar:
    st.markdown("# Choose an insight you'd like to explore:")
    selected_insight = pills(
        label="Available Insights: ",
        label_visibility="collapsed",
        options=insight_names,
        index=None,
    )

    st.markdown(f"# Would you like to view a year other than {max(years)}?")
    year_option = pills(
        f"Are you interested in seeing a year other than {max(years)}?",
        options=[year for year in years[::-1]],
        label_visibility="collapsed",
    )

if "insights" not in st.session_state:
    st.session_state["insights"] = Insights(
        steps_by_year=steps_by_year_insight_data,
        steps_by_month=steps_by_month_insight_data,
        steps_by_day=steps_by_day_insight_data,
        year=year_option,
    )

insights: Insights = st.session_state["insights"]
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
insights_map = {tab: fn for tab, fn in insights_list}


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
        if f"{selected_insight}_{year_option}" in st.session_state:
            insight: InsightsFormatter = st.session_state[
                f"{selected_insight}_{year_option}"
            ]
            previous_placeholder.info("This insight was previously determined")
        else:
            insight = insight_function()
            st.session_state[f"{selected_insight}_{year_option}"] = insight

    title_placeholder.header(insight.title)
    highlight_placeholder.subheader(insight.highlight)
    fun_placeholder.write(insight.fun_to_know)
    challenge_placeholder.write(insight.challenge)


def follow_up(disabled: bool = False):
    question_placeholder = st.empty()
    chat_input_placeholder = st.empty()

    question_placeholder.subheader("Have a Question About Your Insight?")

    with st.chat_message("assistant"):
        st.write("Is there anything you would like to know about your insight?")

    chat_input = chat_input_placeholder.chat_input(max_chars=100, disabled=disabled)

    if chat_input:
        with st.chat_message("user"):
            st.write(chat_input)

        response = insights.follow_up(input=chat_input).response

        with st.chat_message("assistant"):
            st.write(response)

    st.session_state["disabled"] = True


if selected_insight:
    if f"{selected_insight}_{year_option}" not in st.session_state:
        st.session_state["disabled"] = False

    display_insight(selected_insight=selected_insight)
    follow_up(st.session_state.get("disabled", False))
