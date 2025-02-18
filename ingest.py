import os
import duckdb
import pandas as pd

data_dir = "data/20250218135116"
files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

with duckdb.connect("data/health.db") as conn:
    for file in files:
        table_name = file.split(".")[0]
        file_path = f"{data_dir}/{file}"

        data = pd.read_csv(file_path, header=1, index_col=None)

        data.reset_index(inplace=True)
        columns = [col.strip() for col in data.columns if col != "index"]

        data = data.iloc[:, :-1]
        data.columns = columns

        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM data")
