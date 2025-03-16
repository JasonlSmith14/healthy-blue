import streamlit as st
import subprocess

from db.database import Database
from ingest.ingest import Ingest
from models.city import City
from sorting_data import sorting_data
from util import compile_run_dbt

data_directory = "data"
raw_data_directory = "data/raw"
clean_data_directory = "data/clean"

cities = [
    City(-26.2041, 28.0473, 1753, "Johannesburg"),
    City(-29.8587, 31.0218, 8, "Durban"),
    City(-33.9249, 18.4241, 42, "Cape Town"),
]

files = st.file_uploader(
    label="Upload your health data files", accept_multiple_files=True
)

option = st.selectbox(
    "What was your primary location?",
    (city.location_name for city in cities),
)


if st.button(label="Upload files"):
    with st.status("Creating Insights..."):
        if not files:
            raise ValueError("Files were not uploaded")

        city = next((city for city in cities if city.location_name == option), None)

        for file in files:
            with open(f"{raw_data_directory}/{file.name}", "wb") as f:
                bytes_data = file.read()
                f.write(bytes_data)

        uploaded_folder = ""

        cleaned_data_path = sorting_data(
            raw_data_directory=raw_data_directory,
            cleaned_data_directory=clean_data_directory,
            uploaded_folder=uploaded_folder,
        )

        db_path = f"{data_directory}/health.db"
        database = Database(db_url=f"sqlite:///{db_path}")
        ingest = Ingest(data_directory=clean_data_directory, database=database, city=city)

        ingest.ingest_steps(
            folder_path=cleaned_data_path, steps_file_name="step_daily_trend.csv"
        )
        ingest.ingest_weather()

        compile_command = ["dbt", "compile"]
        run_command = ["dbt", "run"]

        compile_run_dbt(compile_command=compile_command, run_command=run_command)
