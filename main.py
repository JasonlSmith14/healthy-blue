import os
import streamlit as st

from ingest.ingest import Ingest
from models.city import City
from util import run_dbt
from config import database, data_directory

st.set_page_config(layout="wide")

st.sidebar.page_link("main.py", label="Upload Your Data")
st.sidebar.page_link("pages/insights.py", label="Your Insights")

raw_data_directory = f"{data_directory}/raw"
clean_data_directory = f"{data_directory}/clean"

try:
    os.mkdir(f"{raw_data_directory}/")
except FileExistsError:
    print(f"Folder: {raw_data_directory} already exists")

try:
    os.mkdir(f"{clean_data_directory}/")
except FileExistsError:
    print(f"Folder: {clean_data_directory} already exists")

st.info(
    "Please note that the file needed is called: com.samsung.shealth.step_daily_trend.csv"
)
file = st.file_uploader(
    label="Upload Your Health Data",
)

cities = [
    City(-26.2041, 28.0473, 1753, "Johannesburg"),
    City(-29.8587, 31.0218, 8, "Durban"),
    City(-33.9249, 18.4241, 42, "Cape Town"),
]
option = st.selectbox(
    "What was your primary location?",
    (city.location_name for city in cities),
)


if st.button(label="Upload File"):
    with st.status("Ingesting Health Data..."):
        if not file:
            raise ValueError("Files were not uploaded")

        city = next((city for city in cities if city.location_name == option), None)

        with open(f"{raw_data_directory}/{file.name}", "wb") as f:
            bytes_data = file.read()
            f.write(bytes_data)

        ingest = Ingest(
            data_directory=clean_data_directory, database=database, city=city
        )
        ingest.sorting_data(
            raw_data_directory=raw_data_directory,
            cleaned_data_directory=clean_data_directory,
            uploaded_file=file.name,
        )
        ingest.ingest_steps(steps_file_name="step_daily_trend.csv")
        ingest.ingest_weather()

        run_command = ["dbt", "run"]
        run_dbt(run_command=run_command, dbt_project_name="healthy_blue")

        st.switch_page("pages/insights.py")
