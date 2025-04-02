from dataclasses import dataclass
from datetime import datetime
from typing import List
import pandas as pd


@dataclass
class InsightData:
    dataframe: pd.DataFrame
    date_column: str
    date_format: str

    def years_available(self):
        years: List[int] = list(
            set(
                list(
                    self.dataframe[self.date_column].apply(
                        lambda x: int(datetime.strptime(x, self.date_format).year)
                    )
                )
            )
        )
        years.sort()
        return years
