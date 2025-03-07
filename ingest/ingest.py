from datetime import datetime
import pandas as pd
from pydantic import BaseModel
from sqlalchemy import func, select
from meteostat import Point, Daily

from models.models import Steps, Weather
from db.database import Database


class Ingest(BaseModel):
    data_directory: str
    database: Database

    class Config:
        arbitrary_types_allowed = True

    def ingest_steps(self, folder_path: str, steps_file_name: str):

        file_path = f"{self.data_directory}/{folder_path}/{steps_file_name}"

        data = pd.read_csv(file_path, index_col=0)
        data["run_id"] = folder_path

        with self.database.get_session() as conn:
            try:
                data.to_sql(
                    Steps.__tablename__,
                    self.database.engine,
                    if_exists="append",
                    index=False,
                )
            except Exception as e:
                print(e)

    def ingest_weather(
        self,
        latitude: float = -26.2041,
        longitude: float = 28.0473,
        altitude: int = 1753,
        location_name: str = "Johannesburg",
        default_start_date: str = "2015-01-01",
    ):
        with self.database.get_session() as conn:
            query = select(func.max(Weather.time))
            output = conn.execute(query)

        weather_time = output.fetchall()[0][0]

        # Set time period
        start = (
            datetime.strptime(weather_time, "%Y-%m-%d %H:%M:%S.%f")
            if weather_time
            else datetime.strptime(default_start_date, "%Y-%m-%d")
        )
        end = datetime.now()

        if start.date() != end.date():
            location_point = Point(latitude, longitude, altitude)

            data = Daily(location_point, start, end)
            data = data.fetch()

            data.reset_index(inplace=True)
            data = data.iloc[1:]
            data["location"] = location_name

            data.to_sql(
                Weather.__tablename__,
                con=self.database.engine,
                if_exists="append",
                index=False,
            )
