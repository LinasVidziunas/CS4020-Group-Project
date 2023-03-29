import pandas as pd

def percentage_missing_values_per_column(df: pd.DataFrame) -> pd.Series:
    percent_missing: pd.Series = df.isnull().sum() * 100 / len(df)
    return percent_missing.sort_values(ascending=False)