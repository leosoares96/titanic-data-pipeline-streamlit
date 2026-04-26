import pandas as pd

def extract():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    df.to_csv("data/raw/titanic.csv", index=False)
    return df