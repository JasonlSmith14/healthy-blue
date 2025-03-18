import pandas as pd
import streamlit as st

from insights.model import Model
from insights.formatting import ResponseFormatter


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
        self.total_steps = "total_steps"

        self.units = (
            "The units for the input data are as follows:"
            " Total steps are measured in steps, speed in meters per second (m/s), and total distance in meters (m). "
            "Calories burned are recorded in kilocalories (kcal). "
            "Temperature readings, including average, minimum, and maximum temperatures, are in degrees Celsius (°C). "
            "Precipitation and Rainfall are measured in millimeters (mm), while wind speed is recorded in meters per second (m/s). "
            "Average and maximum steps are measured in steps, while average and maximum speeds are in meters per second (m/s). "
            "Distance metrics, including average and maximum distances, are in meters (m). "
            "Calories burned, including average and maximum values, are in kilocalories (kcal). "
        )

        self.model = Model(
            system_prompt=f"""
                        You are an expert in transforming **personal health data and weather trends** into fun and engaging summaries—like Spotify Wrapped, but for wellness! 

                        🎯 **Your Goal:** 
                        Create vibrant, **highly personalized** insights that celebrate user achievements and make their journey exciting and motivating.

                        ✨ **Tone & Style:** 
                        - Positive, playful, and **encouraging**—think of it as a **highlight reel** of their progress!
                        - Keep language **enthusiastic and energetic** to make users feel accomplished.
                        - Use **short, engaging sentences** with a lighthearted tone.

                        📊 **Key Considerations:** 
                        - Insights should be **easy to understand**—avoid overly complex stats.
                        - **Data applies to general movement and activity**—do not assume a specific type of exercise or sport.
                        - **Units for input data**:  
                        ```
                        {self.units}
                        ```
                        - Format numbers clearly for quick readability.
                        - Include **fun facts and motivating challenges** to inspire continued progress.
                        - **Use emojis freely** to enhance engagement and make the summary more shareable. 🎉

                        Your insights should feel **exciting, rewarding, and worth celebrating**! 🚀
                        """
        )

    def _human_readable(self, num: int, distance_flag: bool = False):
        if distance_flag:
            return f"{num/1_000:.1f} km"
        else:
            if num >= 1_000_000:
                return f"{num/1_000_000:.1f}M"
            elif num >= 1_000:
                return f"{num/1_000:.1f}K"
        return str(num)

    def _write_output(self, input: str):
        previous_placeholder = st.empty()
        title_placeholder = st.empty()
        highlight_placeholder = st.empty()
        fun_placeholder = st.empty()
        challenge_placeholder = st.empty()

        if input in st.session_state:
            output: ResponseFormatter = st.session_state[input]
            previous_placeholder.info("This insight was previously determined")
            title_placeholder.header(output.title)
            highlight_placeholder.subheader(output.highlight)
            fun_placeholder.write(output.fun_to_know)
            challenge_placeholder.write(output.challenge)
        else:
            for output in self.model.generate_output(user_prompt=input):
                title_placeholder.header(output.title)
                highlight_placeholder.subheader(output.highlight)
                fun_placeholder.write(output.fun_to_know)
                challenge_placeholder.write(output.challenge)

            st.session_state[input] = output

    def _filter_for_year(self, data: pd.DataFrame, date_column: str, format: str):
        data[date_column] = pd.to_datetime(data[date_column], format=format)
        data = data[data[date_column].dt.year == int(self.year_option)]
        return data

    def years_available(self):
        years = self.steps_by_year[self.steps_by_year_date_column]
        self.year_option = st.selectbox(
            "Which year are you interested in seeing?",
            placeholder="Choose a year",
            options=(year for year in years),
        )
        st.session_state[self.year_option] = []

    def day_with_most_steps(self):
        data = self.steps_by_day.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_day_date_column, format="%Y-%m-%d"
        )
        row = data.loc[data[self.total_steps].idxmax()]

        self._write_output(f"This is the day the user took the most steps: {row}")

    def day_with_greatest_distance(self):
        data = self.steps_by_day.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_day_date_column, format="%Y-%m-%d"
        )
        row = data.loc[data[self.total_distance].idxmax()]

        self._write_output(
            f"This is the day the user traveled the furthest distance: {row}"
        )

    def month_with_most_steps(self):
        data = self.steps_by_month.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_month_date_column, format="%Y-%m"
        )
        row = data.loc[data[self.total_steps].idxmax()]

        self._write_output(f"This is the month the user took the most steps: {row}")
