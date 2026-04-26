from src.extract import extract
from src.transform import transform
from src.load import load
from src.config import load_config
from src.logger import get_logger

def run():
    config = load_config()
    logger = get_logger()

    df = extract(config, logger)
    transform(df, config, logger)
    load(config, logger)

if __name__ == "__main__":
    run()