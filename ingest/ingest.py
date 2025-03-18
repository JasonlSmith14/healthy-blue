from datetime import datetime
import os
import pandas as pd
from pydantic import BaseModel
from meteostat import Point, Daily

from models.city import City
from models.models import Steps, Weather
from db.database import Database


class Ingest(BaseModel):
    data_directory: str
    database: Database
    city: City
    creation_date: str = None

    class Config:
        arbitrary_types_allowed = True

    def sorting_data(
        self, raw_data_directory: str, cleaned_data_directory: str, uploaded_file: str
    ):
        self.creation_date = uploaded_file.split(".")[-2]
        cleaned_data_path = f"{cleaned_data_directory}/{self.creation_date}"

        try:
            os.mkdir(f"{cleaned_data_path}/")
        except FileExistsError:
            print(f"Folder: {cleaned_data_path} already exists")

        new_file_name = uploaded_file.split(".")[-3]
        data = pd.read_csv(
            f"{raw_data_directory}/{uploaded_file}",
            header=1,
            index_col=None,
        )

        data.reset_index(inplace=True)
        columns = [col.strip() for col in data.columns if col != "index"]

        data = data.iloc[:, :-1]
        data.columns = columns

        data.to_csv(f"{cleaned_data_path}/{new_file_name}.csv")

    def ingest_steps(self, steps_file_name: str):

        file_path = f"{self.data_directory}/{self.creation_date}/{steps_file_name}"

        data = pd.read_csv(file_path, index_col=0)
        data["run_id"] = self.creation_date
        data["location"] = self.city.location_name

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
        default_start_date: str = "2015-01-01",
    ):

        weather_data = pd.read_sql(
            f"SELECT MAX(time) AS max_time FROM {Weather.__tablename__} WHERE location = :location",
            self.database.engine,
            params={"location": self.city.location_name},
        )

        weather_time = weather_data.iloc[0, 0]

        start = (
            datetime.strptime(weather_time, "%Y-%m-%d %H:%M:%S.%f")
            if weather_time
            else datetime.strptime(default_start_date, "%Y-%m-%d")
        )
        end = datetime.now()

        if start.date() != end.date():
            location_point = Point(
                self.city.latitude, self.city.longitude, self.city.altitude
            )

            data = Daily(location_point, start, end)
            data = data.fetch()

            data.reset_index(inplace=True)
            data = data.iloc[1:]
            data["location"] = self.city.location_name

            try:
                data.to_sql(
                    Weather.__tablename__,
                    con=self.database.engine,
                    if_exists="append",
                    index=False,
                )
            except Exception as e:
                print(e)
