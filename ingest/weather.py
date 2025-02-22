from datetime import datetime
from meteostat import Point, Daily
import sqlite3

from db.database import Database

# SQLite connection
db_path = "data/health.db"
db_url = f"sqlite:///{db_path}"
database = Database(db_url=db_url)
database.create_tables()

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    query = f"SELECT MAX(time) FROM weather"

    cursor.execute(query)
    weather_time = cursor.fetchall()[0][0]

    # Set time period
    start = (
        datetime.strptime(weather_time, "%Y-%m-%d")
        if weather_time
        else datetime.strptime("2015-01-01", "%Y-%m-%d")
    )
    end = datetime.now()

    if start.date() != end.date():

        # Create Point for Johannesburg, South Africa
        johannesburg = Point(
            -26.2041, 28.0473, 1753
        )  # Latitude, Longitude, Elevation (m)

        data = Daily(johannesburg, start, end)
        data = data.fetch()

        data.reset_index(inplace=True)
        data = data.iloc[1:]
        data["time"] = data["time"].astype(str)

        data.to_sql("weather", con=conn, if_exists="append", index=False)
