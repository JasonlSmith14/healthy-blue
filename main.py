from db.database import Database
from ingest.ingest import Ingest
from sorting_data import sorting_data

data_directory = "data"
raw_data_directory = "data/raw"
clean_data_directory = "data/clean"
# This assumes a folder is uploaded
uploaded_folder = "samsunghealth_jasonlsmith14_20250218135116"

cleaned_data_path = sorting_data(
    raw_data_directory=raw_data_directory,
    cleaned_data_directory=clean_data_directory,
    uploaded_folder=uploaded_folder,
)

db_path = f"{data_directory}/health.db"
database = Database(db_url=f"sqlite:///{db_path}")
ingest = Ingest(data_directory=clean_data_directory, database=database)

ingest.ingest_steps(
    folder_path=cleaned_data_path, steps_file_name="step_daily_trend.csv"
)
ingest.ingest_weather()
