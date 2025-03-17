import time
import pandas as pd
import streamlit as st


class Insights:
    def __init__(
        self,
        steps_by_day: pd.DataFrame,
        steps_by_month: pd.DataFrame,
        steps_by_year: pd.DataFrame,
    ):
        self.steps_by_day = steps_by_day
        self.steps_by_month = steps_by_month
        self.steps_by_year = steps_by_year

    def _human_readable(self, num: int):
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return str(num)

    def _write_output(self, input: str):
        st.header(input)

    def _formatting_for_month_chart(self, data: pd.DataFrame):
        data["month_of_the_year"] = pd.to_datetime(
            data["month_of_the_year"], format="%Y-%m"
        )
        data = data[data["month_of_the_year"].dt.year == int(self.year_option)]

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

        data["month_of_the_year"] = pd.Categorical(
            data["month_of_the_year"], categories=month_order, ordered=True
        )

        data = data.sort_values("month_of_the_year")

        return data

    def years_available(self):
        years = self.steps_by_year["year"]
        self.year_option = st.selectbox(
            "Which year are you interested in seeing?",
            placeholder="Choose a year",
            options=(year for year in years),
        )

    def day_with_most_steps(self):
        data = self.steps_by_day.copy()
        data["recorded_date"] = pd.to_datetime(data["recorded_date"], format="%Y-%m-%d")
        data = data[data["recorded_date"].dt.year == int(self.year_option)]
        row = data.loc[data["total_steps"].idxmax()]

        self._write_output(
            f"You took the most steps on {row["recorded_date"].strftime("%d %B")} with a total of {self._human_readable(row["total_steps"])} steps"
        )

    def month_with_most_steps(self):
        data = self.steps_by_month.copy()
        data["month_of_the_year"] = pd.to_datetime(
            data["month_of_the_year"], format="%Y-%m"
        )
        data = data[data["month_of_the_year"].dt.year == int(self.year_option)]
        row = data.loc[data["total_steps"].idxmax()]

        self._write_output(
            f"You took the most steps in {row["month_of_the_year"].strftime("%B")} with a total of {self._human_readable(row["total_steps"])} steps"
        )

    def average_max_min_steps_by_month(self):
        data = self.steps_by_month.copy()
        data = self._formatting_for_month_chart(data=data)

        st.line_chart(
            data=data,
            x="month_of_the_year",
            y=["average_steps", "maximum_steps"],
            x_label="Month",
            y_label="Steps",
        )

    def average_max_min_distance_by_month(self):
        data = self.steps_by_month.copy()
        data = self._formatting_for_month_chart(data=data)

        st.line_chart(
            data=data,
            x="month_of_the_year",
            y=["average_distance", "maximum_distance"],
            x_label="Month",
            y_label="Distance (m)",
        )

    def distance_over_the_year(self):
        data = self.steps_by_month.copy()
        data = self._formatting_for_month_chart(data=data)

        st.bar_chart(
            data=data,
            x="month_of_the_year",
            y=["total_distance"],
            x_label="Month",
            y_label="Distance (m)",
        )

    def steps_over_the_year(self):
        data = self.steps_by_month.copy()
        data = self._formatting_for_month_chart(data=data)

        st.bar_chart(
            data=data,
            x="month_of_the_year",
            y="total_steps",
            x_label="Month",
            y_label="Steps",
        )

    def steps_over_the_years(self):
        data = self.steps_by_year.copy()

        st.bar_chart(
            data=data,
            x="year",
            y="total_steps",
            x_label="Year",
            y_label="Steps",
        )
