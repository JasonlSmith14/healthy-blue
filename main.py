import streamlit as st

from ingest.ingest import Ingest
from models.city import City
from ingest.sorting_data import sorting_data
from util import run_dbt
from config import database, data_directory

st.set_page_config(layout="wide")

st.sidebar.page_link("main.py", label="Upload Your Data")
st.sidebar.page_link("pages/insights.py", label="Your Insights")

raw_data_directory = f"{data_directory}/raw"
clean_data_directory = f"{data_directory}/clean"

files = st.file_uploader(
    label="Upload your health data files", accept_multiple_files=True
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


if st.button(label="Upload files"):
    with st.status("Ingesting Health Data..."):
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

        ingest = Ingest(
            data_directory=clean_data_directory, database=database, city=city
        )

        ingest.ingest_steps(
            folder_path=cleaned_data_path, steps_file_name="step_daily_trend.csv"
        )
        ingest.ingest_weather()

        run_command = ["dbt", "run"]

        run_dbt(run_command=run_command, dbt_project_name="healthy_blue")

        st.switch_page("pages/insights.py")
