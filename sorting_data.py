import os

files = [f for f in os.listdir("data/")]
creation_dates = {file.split(".")[-2] for file in files}

for creation_date in creation_dates:
    os.mkdir(f"data/{creation_date}/")

for file in files:
    os.rename(f"data/{file}", f"data/{file.split(".")[-2]}/{file.split(".")[-3]}.csv")
