import os

import pandas as pd


def sorting_data(data_directory: str):
    files = [f for f in os.listdir(data_directory) if f.endswith("csv")]

    if not files:
        print("No files found to be sorted")
        return

    creation_dates = {file.split(".")[-2] for file in files}

    for creation_date in creation_dates:
        os.mkdir(f"{data_directory}{creation_date}/")

    for file in files:
        os.rename(
            f"{data_directory}{file}",
            f"{data_directory}{file.split(".")[-2]}/{file.split(".")[-3]}.csv",
        )

        data = pd.read_csv(f"{data_directory}{file}", header=1, index_col=None)

        data.reset_index(inplace=True)
        columns = [col.strip() for col in data.columns if col != "index"]

        data = data.iloc[:, :-1]
        data.columns = columns

        data.to_csv(f"{data_directory}{file}")
