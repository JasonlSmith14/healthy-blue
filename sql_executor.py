import sqlite3

import pandas as pd

db_path = "data/health.db"
query = """
select * from silver_steps_and_weather limit 10
"""

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute(query)
    items = cursor.fetchall()

    print(pd.DataFrame(items))
    
