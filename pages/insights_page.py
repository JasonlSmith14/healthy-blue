import pandas as pd
from config import database
import streamlit as st

from util import human_readable
st.set_page_config(layout="wide")

if "gold_steps_by_year" not in st.session_state:
    gold_steps_by_year = pd.read_sql(
        "SELECT * FROM gold_steps_by_year", database.engine
    )
    st.session_state["gold_steps_by_year"] = gold_steps_by_year

if "gold_steps_by_month" not in st.session_state:
    gold_steps_by_month = pd.read_sql(
        "SELECT * FROM gold_steps_by_month", database.engine
    )
    st.session_state["gold_steps_by_month"] = gold_steps_by_month

if "gold_steps_by_day" not in st.session_state:
    gold_steps_by_day = pd.read_sql("SELECT * FROM gold_steps_by_day", database.engine)
    st.session_state["gold_steps_by_day"] = gold_steps_by_day


gold_steps_by_year: pd.DataFrame = st.session_state["gold_steps_by_year"]
gold_steps_by_month: pd.DataFrame = st.session_state["gold_steps_by_month"]
gold_steps_by_day: pd.DataFrame = st.session_state["gold_steps_by_day"]

years = gold_steps_by_year["year"]
year_option = st.selectbox(
    "Which year are you interested in seeing?",
    placeholder="Choose a year",
    options=(year for year in years),
)

day_with_most_steps_tab, month_with_most_steps_tab, steps_over_the_year = st.tabs(
    [
        "Your day with most steps",
        "Your month with most steps",
        f"Your steps over the year",
    ]
)

with day_with_most_steps_tab:
    data = gold_steps_by_day.copy()
    data["recorded_date"] = pd.to_datetime(data["recorded_date"], format="%Y-%m-%d")
    data = data[data["recorded_date"].dt.year == int(year_option)]
    row = data.loc[data["total_steps"].idxmax()]

    st.write(
        f"You took the most steps on {row["recorded_date"].strftime("%d %B")} with a total of {human_readable(row["total_steps"])} steps"
    )

with month_with_most_steps_tab:
    data = gold_steps_by_month.copy()
    data["month_of_the_year"] = pd.to_datetime(
        data["month_of_the_year"], format="%Y-%m"
    )
    data = data[data["month_of_the_year"].dt.year == int(year_option)]
    row = data.loc[data["total_steps"].idxmax()]

    st.write(
        f"You took the most steps in {row["month_of_the_year"].strftime("%B")} with a total of {human_readable(row["total_steps"])} steps"
    )


with steps_over_the_year:
    data = gold_steps_by_month.copy()
    data["month_of_the_year"] = pd.to_datetime(
        data["month_of_the_year"], format="%Y-%m"
    )
    data = data[data["month_of_the_year"].dt.year == int(year_option)]
    data["month_of_the_year"] = data["month_of_the_year"].apply(
        lambda x: x.strftime("%B")
    )

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    # Convert "month" column to categorical with custom order
    data["month_of_the_year"] = pd.Categorical(data["month_of_the_year"], categories=month_order, ordered=True)

    # Sort the data according to the defined order
    data = data.sort_values("month_of_the_year")

    st.bar_chart(data=data, x="month_of_the_year", y="total_steps", x_label="Month", y_label="Steps")
