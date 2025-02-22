import os

import pandas as pd

data_dir = "data/"
folders = [f for f in os.listdir(data_dir) if os.path.isdir(f"{data_dir}/{f}")]
for folder in folders:
    for file in os.listdir(f"{data_dir}{folder}/"):
        data = pd.read_csv(f"{data_dir}{folder}/{file}", header=1, index_col=None)

        data.reset_index(inplace=True)
        columns = [col.strip() for col in data.columns if col != "index"]

        data = data.iloc[:, :-1]
        data.columns = columns

        data.to_csv(f"{data_dir}{folder}/{file}")
