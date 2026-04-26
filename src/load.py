import sqlite3
import pandas as pd

def load(config, logger):
    logger.info("Loading data into SQLite")

    df = pd.read_parquet(config["paths"]["processed"])

    conn = sqlite3.connect(config["database"]["path"])
    df.to_sql(config["database"]["table"], conn, if_exists="replace", index=False)
    conn.close()

    logger.info("Data loaded successfully")