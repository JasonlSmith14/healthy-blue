import os
import sqlite3
import pandas as pd

from db.database import Database

# SQLite connection
db_path = "data/health.db"
db_url = f"sqlite:///{db_path}"
database = Database(db_url=db_url)
database.create_tables()

data_dir = "data/"
folders = [f for f in os.listdir(data_dir) if os.path.isdir(f"{data_dir}/{f}")]
folders.sort()

latest_folder = folders[-1]
file_path = f"{data_dir}{latest_folder}/step_daily_trend.csv"

data = pd.read_csv(file_path, index_col=0)

datauuids = list(data["datauuid"])

# Connect to SQLite and execute query
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Create placeholders for the number of UUIDs
    placeholders = ",".join("?" for _ in datauuids)
    query = f"SELECT datauuid FROM steps WHERE datauuid IN ({placeholders})"

    # Execute the query with datauuids
    cursor.execute(query, datauuids)
    existent_entries = cursor.fetchall()

    # Extract UUIDs from the result (existent_entries is a list of tuples)
    existent_uuids = [entry[0] for entry in existent_entries]

    # Filter the data to include only new UUIDs
    entries_to_add = [
        datauuid for datauuid in datauuids if datauuid not in existent_uuids
    ]

    # Filter the DataFrame to include only rows with the UUIDs to add
    data_to_add = data[data["datauuid"].isin(entries_to_add)]

    # Insert the new data into the table
    data_to_add.to_sql("steps", conn, if_exists="append", index=False)
