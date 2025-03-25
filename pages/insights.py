import time
import pandas as pd
from config import database
import streamlit as st
from insights.formatting import ResponseFormatter
from insights.insights import Insights
from models.insight_data import InsightData

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

years = insights.years_available()
year_option = st.sidebar.selectbox(
    f"Are you interested in seeing a year other than {max(years)}?",
    placeholder="Choose a year",
    options=(year for year in years[::-1]),
)


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

insights_map = {
    day_with_most_steps_tab: insights.day_with_most_steps,
    day_with_greatest_distance_tab: insights.day_with_greatest_distance,
    month_with_most_steps_tab: insights.month_with_most_steps,
    hottest_day_tab: insights.hottest_day,
    coldest_day_tab: insights.coldest_day,
    day_with_least_steps_tab: insights.day_with_least_steps,
    day_with_smallest_distance_tab: insights.day_with_smallest_distance,
    month_with_least_steps_tab: insights.month_with_least_steps,
}

if "insight_number" not in st.session_state:
    st.session_state["insight_number"] = 0


@st.fragment
def display_insight():
    rerun = False

    insight_pkaceholder = st.empty()
    previous_placeholder = st.empty()
    title_placeholder = st.empty()
    highlight_placeholder = st.empty()
    fun_placeholder = st.empty()
    challenge_placeholder = st.empty()

    insight_name = insight_names[st.session_state["insight_number"]]
    insight_function = insights_map[insight_name]

    insight_pkaceholder.markdown(f"# {insight_name}")
    with st.spinner("Generating insight...", show_time=True):
        if insight_name in st.session_state:
            insight: ResponseFormatter = st.session_state[insight_name]
            previous_placeholder.info("This insight was previously determined")
        else:
            insight = insight_function()
            st.session_state[insight_name] = insight

    title_placeholder.header(insight.title)
    highlight_placeholder.subheader(insight.highlight)
    fun_placeholder.write(insight.fun_to_know)
    challenge_placeholder.write(insight.challenge)

    col1, col2 = st.columns(2, gap="small")
    if st.session_state["insight_number"] != 0:
        with col1:
            if st.button(
                "⬅️ Previous", key=f"previous_{st.session_state["insight_number"]}"
            ):
                st.session_state["insight_number"] = (
                    st.session_state["insight_number"] - 1
                )
                rerun = True

    if st.session_state["insight_number"] != len(insight_names):
        with col2:
            if st.button("Next ➡️", key=f"next_{st.session_state["insight_number"]}"):
                st.session_state["insight_number"] = (
                    st.session_state["insight_number"] + 1
                )
                rerun = True
    if rerun:
        st.rerun(scope="fragment")


display_insight()

# Look more at data behind your insights - expander with more raw data
# Classify chain as good/bad - question why it was bad: Becomes interactive; provide suggestion on how to improve
