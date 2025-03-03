import os

import pandas as pd


def sorting_data(
    raw_data_directory: str, cleaned_data_directory: str, uploaded_folder: str
):
    files = [
        f
        for f in os.listdir(f"{raw_data_directory}/{uploaded_folder}")
        if f.endswith("csv")
    ]

    creation_dates = {file.split(".")[-2] for file in files}

    if len(creation_dates) != 1:
        raise ValueError(
            f"More than one date appeared for the folder: {uploaded_folder}"
        )

    creation_date = creation_dates.pop()
    cleaned_data_path = f"{cleaned_data_directory}/{creation_date}"

    try:
        os.mkdir(f"{cleaned_data_path}/")
    except FileExistsError as fee:
        print(f"Folder: {cleaned_data_path} already exists")

    for file in files:

        new_file_name = file.split(".")[-3]
        data = pd.read_csv(
            f"{f"{raw_data_directory}/{uploaded_folder}"}/{file}",
            header=1,
            index_col=None,
        )

        data.reset_index(inplace=True)
        columns = [col.strip() for col in data.columns if col != "index"]

        data = data.iloc[:, :-1]
        data.columns = columns

        data.to_csv(f"{cleaned_data_path}/{new_file_name}.csv")

    return creation_date
