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

        self.steps_by_day_date_column = "recorded_date"
        self.steps_by_month_date_column = "month_of_the_year"
        self.steps_by_year_date_column = "year"

        self.total_distance = "total_distance"
        self.maximum_distance = "maximum_distance"
        self.average_distance = "average_distance"

        self.total_steps = "total_steps"
        self.maximum_steps = "maximum_steps"
        self.average_steps = "average_steps"

    def _human_readable(self, num: int):
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return str(num)

    def _write_output(self, input: str):
        st.header(input)

    def _filter_for_year(self, data: pd.DataFrame, date_column: str, format: str):
        data[date_column] = pd.to_datetime(data[date_column], format=format)
        data = data[data[date_column].dt.year == int(self.year_option)]
        return data

    def _formatting_for_month_chart(self, data: pd.DataFrame):
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_month_date_column, format="%Y-%m"
        )

        data[self.steps_by_month_date_column] = data[
            self.steps_by_month_date_column
        ].apply(lambda x: x.strftime("%B"))

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

        data[self.steps_by_month_date_column] = pd.Categorical(
            data[self.steps_by_month_date_column], categories=month_order, ordered=True
        )

        data = data.sort_values(self.steps_by_month_date_column)

        return data

    def years_available(self):
        years = self.steps_by_year[self.steps_by_year_date_column]
        self.year_option = st.selectbox(
            "Which year are you interested in seeing?",
            placeholder="Choose a year",
            options=(year for year in years),
        )

    def day_with_most_steps(self):
        data = self.steps_by_day.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_day_date_column, format="%Y-%m-%d"
        )
        row = data.loc[data[self.total_steps].idxmax()]

        self._write_output(
            f"You took the most steps on {row[self.steps_by_day_date_column].strftime("%d %B")} with a total of {self._human_readable(row[self.total_steps])} steps"
        )

    def month_with_most_steps(self):
        data = self.steps_by_month.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_month_date_column, format="%Y-%m"
        )
        row = data.loc[data[self.total_steps].idxmax()]

        self._write_output(
            f"You took the most steps in {row[self.steps_by_month_date_column].strftime("%B")} with a total of {self._human_readable(row[self.total_steps])} steps"
        )

    def average_max_min_steps_by_month(self):
        data = self.steps_by_month.copy()
        data = self._formatting_for_month_chart(data=data)

        st.line_chart(
            data=data,
            x=self.steps_by_month_date_column,
            y=[self.average_steps, self.maximum_steps],
            x_label="Month",
            y_label="Steps",
        )

    def average_max_min_distance_by_month(self):
        data = self.steps_by_month.copy()
        data = self._formatting_for_month_chart(data=data)

        st.line_chart(
            data=data,
            x=self.steps_by_month_date_column,
            y=[self.average_distance, self.maximum_distance],
            x_label="Month",
            y_label="Distance (m)",
        )

    def distance_over_the_year(self):
        data = self.steps_by_month.copy()
        data = self._formatting_for_month_chart(data=data)

        st.bar_chart(
            data=data,
            x=self.steps_by_month_date_column,
            y=[self.total_distance],
            x_label="Month",
            y_label="Distance (m)",
        )

    def steps_over_the_year(self):
        data = self.steps_by_month.copy()
        data = self._formatting_for_month_chart(data=data)

        st.bar_chart(
            data=data,
            x=self.steps_by_month_date_column,
            y=self.total_steps,
            x_label="Month",
            y_label="Steps",
        )

    def steps_over_the_years(self):
        data = self.steps_by_year.copy()

        st.bar_chart(
            data=data,
            x=self.steps_by_year_date_column,
            y=self.total_steps,
            x_label="Year",
            y_label="Steps",
        )
