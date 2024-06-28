from pipeline import read_data, clean, consolidation
from llm import create_embeddings
import time

if __name__ == "__main__":
    sources = ["chatgpt", "netflix", "spotify"]
    RUN_OLD_PIPELINE = False
    RUN_EMBEDDINGS = False

    start = time.time()
    for source in sources:
        print(f"Reading data from {source}")
        df = read_data(source)
        df = consolidation(df, source)
        df = clean(df, RUN_OLD_PIPELINE, source)
        if RUN_EMBEDDINGS:
            create_embeddings(df)
        print(f"Data from {source} written to database")
    print(f"Pipeline completed in {time.time() - start} seconds")
