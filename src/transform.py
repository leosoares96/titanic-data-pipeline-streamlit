from src.quality import run_quality_checks
import pandas as pd

def transform(df, config, logger):
    logger.info("Starting transformation")

    # roda qualidade ANTES
    run_quality_checks(df, logger)

    df = df.drop(columns=["Name", "Ticket", "Cabin"])

    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna("Unknown")

    df["is_child"] = df["Age"] < 12
    df["processed_at"] = pd.Timestamp.now()

    df.columns = [c.lower() for c in df.columns]

    df.to_parquet(config["paths"]["processed"], index=False)

    logger.info(f"Processed data saved to {config['paths']['processed']}")

    return df