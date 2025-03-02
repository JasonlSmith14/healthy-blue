from db.database import Database
from ingest.ingest import Ingest
from sorting_data import sorting_data
data_directory = "data/"

sorting_data(data_directory=data_directory)

db_path = "data/health.db"
database = Database(db_url=f"sqlite:///{db_path}")
ingest = Ingest(data_directory=data_directory, database=database)

ingest.ingest_steps(steps_file_name="step_daily_trend.csv")
ingest.ingest_weather()
