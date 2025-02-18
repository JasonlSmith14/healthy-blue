import duckdb
import pandas as pd

sql_query = """
select * from gold_step_daily_trend
"""

with duckdb.connect("data/health.db") as con:
    print(con.sql(sql_query).df())
