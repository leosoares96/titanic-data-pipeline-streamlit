import pandas as pd
import sqlite3

def load():
    df = pd.read_parquet("data/processed/titanic_clean.parquet")
    
    conn = sqlite3.connect("data/titanic.db")
    df.to_sql("passengers", conn, if_exists="replace", index=False)
    conn.close()