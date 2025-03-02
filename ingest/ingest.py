from datetime import datetime
import pandas as pd
from pydantic import BaseModel
from sqlalchemy import select, text
import os
from meteostat import Point, Daily

from models.models import Steps, Weather
from db.database import Database

class Ingest(BaseModel):
    data_directory: str
    database: Database

    class Config:
        arbitrary_types_allowed = True

    def ingest_steps(self, steps_file_name: str):
        folders = [
            f
            for f in os.listdir(self.data_directory)
            if os.path.isdir(f"{self.data_directory}/{f}")
        ]
        folders.sort()

        latest_folder = folders[-1]
        file_path = f"{self.data_directory}{latest_folder}/{steps_file_name}"

        data = pd.read_csv(file_path, index_col=0)

        datauuids = list(data["datauuid"])

        with self.database.get_session() as conn:
            query = select(Steps.datauuid).where(Steps.datauuid.in_(datauuids))
            existent_entries = conn.execute(query).fetchall()

            # Extract UUIDs from the result (existent_entries is a list of tuples)
            existent_uuids = [entry[0] for entry in existent_entries]

            # Filter the data to include only new UUIDs
            entries_to_add = [
                datauuid for datauuid in datauuids if datauuid not in existent_uuids
            ]

            # Filter the DataFrame to include only rows with the UUIDs to add
            data_to_add = data[data["datauuid"].isin(entries_to_add)]

            # Insert the new data into the table
            data_to_add.to_sql(
                Steps.__tablename__,
                self.database.engine,
                if_exists="append",
                index=False,
            )

    def ingest_weather(self, default_start_date: str = "2015-01-01"):
        with self.database.get_session() as conn:
            query = f"SELECT MAX(time) FROM {Weather.__tablename__}"
            output = conn.execute(text(query))

            weather_time = output.fetchall()[0][0]

            # Set time period
            start = (
                datetime.strptime(weather_time, "%Y-%m-%d")
                if weather_time
                else datetime.strptime(default_start_date, "%Y-%m-%d")
            )
            end = datetime.now()

            if start.date() != end.date():

                lat = -26.2041
                lon = 28.0473
                alt = 1753

                location = f"{lat},{lon},{alt}"

                johannesburg = Point(lat, lon, alt)

                data = Daily(johannesburg, start, end)
                data = data.fetch()

                data.reset_index(inplace=True)
                data = data.iloc[1:]
                data["time"] = data["time"].astype(
                    str
                )  # Is this consistent with everything else? Check what is available - Force format and timezone
                data["location"] = location

                data.to_sql(
                    Weather.__tablename__,
                    con=self.database.engine,
                    if_exists="append",
                    index=False,
                )
