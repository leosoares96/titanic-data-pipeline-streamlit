import sqlite3

def load(df):
    conn = sqlite3.connect("data/titanic.db")
    df.to_sql("passengers", conn, if_exists="replace", index=False)
    conn.close()