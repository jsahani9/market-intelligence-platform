import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.extract_market_data import extract_market_data
from scripts.extract_macro_data import extract_macro_data
from scripts.transform_market_data import transform_market_data
from scripts.load_to_postgres import load_to_postgres


def divider(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_pipeline():
    start = time.time()

    divider("STEP 1 — Extract Market Data")
    extract_market_data()

    divider("STEP 2 — Extract Macro Data")
    extract_macro_data()

    divider("STEP 3 — Transform & Compute Metrics")
    transform_market_data()

    divider("STEP 4 — Load to PostgreSQL")
    load_to_postgres()

    elapsed = time.time() - start
    divider(f"Pipeline Complete — {elapsed:.1f}s")
    print("  All data is up to date in market_intelligence DB.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_pipeline()
