from typing import Callable
import pandas as pd

from insights.model import Model
from models.insight_data import InsightData


class Insights:
    def __init__(
        self,
        steps_by_day: InsightData,
        steps_by_month: InsightData,
        steps_by_year: InsightData,
    ):
        self.steps_by_day = steps_by_day
        self.steps_by_month = steps_by_month
        self.steps_by_year = steps_by_year

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

    def _insight_wrapper(
        self,
        metadata: InsightData,
        filter_function: Callable[[pd.DataFrame], pd.Series],
        insight_description: str,
    ):
        data = metadata.dataframe.copy()
        data = self._filter_for_year(
            data=data, date_column=metadata.date_column, format=metadata.date_format
        )
        row = filter_function(data)

        return self._create_insight(f"{insight_description}: {row}")

    def _create_insight(self, input: str):
        return self.model.generate_insight(user_data=input)

    def _filter_for_year(self, data: pd.DataFrame, date_column: str, format: str):
        data[date_column] = pd.to_datetime(data[date_column], format=format)
        data = data[data[date_column].dt.year == int(max(self.years_available()))]
        return data

    def years_available(self):
        years = self.steps_by_year.dataframe[self.steps_by_year.date_column]
        return years

    def day_with_most_steps(self):
        return self._insight_wrapper(
            metadata=self.steps_by_day,
            filter_function=lambda data: data.loc[data[self.total_steps].idxmax()],
            insight_description="This is the day the user took the most steps",
        )

    def day_with_greatest_distance(self):
        return self._insight_wrapper(
            metadata=self.steps_by_day,
            filter_function=lambda data: data.loc[data[self.total_distance].idxmax()],
            insight_description="This is the day the user travelled the furthest distance",
        )

    def day_with_least_steps(self):
        return self._insight_wrapper(
            metadata=self.steps_by_day,
            filter_function=lambda data: data.loc[data[self.total_steps].idxmin()],
            insight_description="This is the day the user took the least steps",
        )

    def day_with_smallest_distance(self):
        return self._insight_wrapper(
            metadata=self.steps_by_day,
            filter_function=lambda data: data.loc[data[self.total_distance].idxmin()],
            insight_description="This is the day the user travelled the smallest distance",
        )

    def month_with_most_steps(self):
        return self._insight_wrapper(
            metadata=self.steps_by_month,
            filter_function=lambda data: data.loc[data[self.total_steps].idxmax()],
            insight_description="This is the month the user took the most steps",
        )

    def month_with_least_steps(self):
        return self._insight_wrapper(
            metadata=self.steps_by_month,
            filter_function=lambda data: data.loc[data[self.total_steps].idxmin()],
            insight_description="This is the month the user took the least steps",
        )

    def coldest_day(self):
        return self._insight_wrapper(
            metadata=self.steps_by_day,
            filter_function=lambda data: data.loc[
                data[self.maximum_temperature].idxmin()
            ],
            insight_description="This is the coldest day of the year for the user",
        )

    def hottest_day(self):
        return self._insight_wrapper(
            metadata=self.steps_by_day,
            filter_function=lambda data: data.loc[
                data[self.maximum_temperature].idxmax()
            ],
            insight_description="This is the hottest day of the year for the user",
        )
