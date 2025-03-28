from dataclasses import dataclass
import pandas as pd


@dataclass
class InsightData:
    dataframe: pd.DataFrame
    date_column: str
    date_format: str
