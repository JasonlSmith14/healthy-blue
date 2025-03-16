from db.database import Database

data_directory = "data"
db_path = f"{data_directory}/health.db"
database = Database(db_url=f"sqlite:///{db_path}")