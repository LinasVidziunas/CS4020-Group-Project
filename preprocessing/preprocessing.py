import pandas as pd
from sklearn.model_selection import train_test_split

def percentage_missing_values_per_column(df: pd.DataFrame) -> pd.Series:
    percent_missing: pd.Series = df.isnull().sum() * 100 / len(df)
    return percent_missing.sort_values(ascending=False)

def get_highly_correlated_columns(df: pd.DataFrame, threshold: int):
    correlation_matrix: pd.DataFrame = df.cor().abs()
    
def split_train_val_test(df: pd.DataFrame, val_size: float, test_size: float):
    train_set, test_set = train_test_split(df, test_size=test_size, random_state=42)
    train_set, val_set = train_test_split(train_set, test_size=val_size, random_state=42)
    return train_set, val_set, test_set

def split_train_test(df: pd.DataFrame, test_size: float):
    train_set, test_set = train_test_split(df, test_size=test_size, random_state=42)
    return train_set, test_set