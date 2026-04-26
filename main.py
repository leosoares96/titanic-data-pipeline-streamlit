from src.extract import extract
from src.transform import transform
from src.load import load

def run():
    df = extract()
    df = transform(df)
    load(df)

if __name__ == "__main__":
    run()