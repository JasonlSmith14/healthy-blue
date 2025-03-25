import pandas as pd
import streamlit as st

from insights.model import Model


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

        self.maximum_temperature = "maximum_temperature"

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
                    Create vibrant, **highly personalized** insights that celebrate user achievements, making their journey exciting and motivating.  
                    The health data should always be the main focus, with weather data used to explain or highlight **why** certain patterns may have occurred. 🌦️  

                    ✨ **Tone & Style:**  
                    - Positive, playful, and **encouraging**—think of it as a **highlight reel** of their progress!  
                    - Keep language **enthusiastic and energetic** to make users feel accomplished.  
                    - Use **short, engaging sentences** with a lighthearted tone.  

                    📊 **Key Considerations:**  
                    - Insights should be **easy to understand**—avoid overly complex stats.  
                    - **Data applies to general movement and activity**—do not assume a specific type of exercise or sport.  
                    - **Weather data should complement the story**, helping explain unusual dips or boosts (e.g., "Rainy days didn’t slow you down! ☔").  
                    - **Units for input data**:  
                    ```
                    {self.units}
                    ```  
                    - Format numbers clearly for quick readability.  
                    - Include **fun facts and motivating challenges** to inspire continued progress.  
                    - Use weather to add context: celebrate pushing through bad weather or relaxing during extreme heat or storms.  
                    - **Use emojis freely** to enhance engagement and make the summary more shareable. 🎉  

                    Your insights should feel **exciting, rewarding, and worth celebrating**! 🚀
                """
        )

    def _create_insight(self, input: str):
        return self.model.generate_output(user_prompt=input)

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

        return self._create_insight(
            f"This is the day the user took the most steps: {row}"
        )

    def day_with_greatest_distance(self):
        data = self.steps_by_day.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_day_date_column, format="%Y-%m-%d"
        )
        row = data.loc[data[self.total_distance].idxmax()]

        return self._create_insight(
            f"This is the day the user travelled the furthest distance: {row}"
        )

    def day_with_least_steps(self):
        data = self.steps_by_day.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_day_date_column, format="%Y-%m-%d"
        )
        row = data.loc[data[self.total_steps].idxmin()]

        return self._create_insight(
            f"This is the day the user took the least steps: {row}"
        )

    def day_with_smallest_distance(self):
        data = self.steps_by_day.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_day_date_column, format="%Y-%m-%d"
        )
        row = data.loc[data[self.total_distance].idxmin()]

        return self._create_insight(
            f"This is the day the user travelled the smallest distance: {row}"
        )

    def month_with_most_steps(self):
        data = self.steps_by_month.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_month_date_column, format="%Y-%m"
        )
        row = data.loc[data[self.total_steps].idxmax()]

        return self._create_insight(
            f"This is the month the user took the most steps: {row}"
        )

    def month_with_least_steps(self):
        data = self.steps_by_month.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_month_date_column, format="%Y-%m"
        )
        row = data.loc[data[self.total_steps].idxmin()]

        return self._create_insight(
            f"This is the month the user took the least steps: {row}"
        )

    def coldest_day(self):
        data = self.steps_by_day.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_day_date_column, format="%Y-%m-%d"
        )
        row = data.loc[data[self.maximum_temperature].idxmin()]

        return self._create_insight(
            f"This is the coldest day of the year for the user: {row}"
        )

    def hottest_day(self):
        data = self.steps_by_day.copy()
        data = self._filter_for_year(
            data=data, date_column=self.steps_by_day_date_column, format="%Y-%m-%d"
        )
        row = data.loc[data[self.maximum_temperature].idxmax()]

        return self._create_insight(
            f"This is the hottest day of the year for the user: {row}"
        )
