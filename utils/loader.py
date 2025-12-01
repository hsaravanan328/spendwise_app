import pandas as pd

def load_transactions(path="data/cleaned.csv"):
    return pd.read_csv(path)
