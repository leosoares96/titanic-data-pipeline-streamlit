import pandas as pd

def extract(config, logger):
    logger.info("Starting extraction")

    df = pd.read_csv(config["data_source"])
    df.to_csv(config["paths"]["raw"], index=False)

    logger.info(f"Raw data saved to {config['paths']['raw']}")
    
    return df