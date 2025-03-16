import pandas as pd
from config import database
import streamlit as st

from util import human_readable

gold_steps_by_year = pd.read_sql("SELECT * FROM gold_steps_by_year", database.engine)
gold_steps_by_month = pd.read_sql("SELECT * FROM gold_steps_by_month", database.engine)
gold_steps_by_day = pd.read_sql("SELECT * FROM gold_steps_by_day", database.engine)

years = gold_steps_by_year["year"]
year_option = st.selectbox(
    "Which year are you interested in seeing?",
    placeholder="Choose a year",
    options=(year for year in years),
)

day_with_most_steps_tab, month_with_most_steps_tab = st.tabs(
    ["Day with most Steps", "Month with most Steps"]
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
    data["month_of_the_year"] = pd.to_datetime(data["month_of_the_year"], format="%Y-%m")
    data = data[data["month_of_the_year"].dt.year == int(year_option)]
    row = data.loc[data["total_steps"].idxmax()]

    st.write(
        f"You took the most steps in {row["month_of_the_year"].strftime("%B")} with a total of {human_readable(row["total_steps"])} steps"
    )
