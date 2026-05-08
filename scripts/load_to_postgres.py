import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER     = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME", "market_intelligence")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

RAW_DIR       = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")

TICKER_METADATA = {
    "AAPL":  {"company_name": "Apple Inc.",                        "category": "Technology", "sector": "Technology",   "asset_type": "Stock"},
    "MSFT":  {"company_name": "Microsoft Corporation",             "category": "Technology", "sector": "Technology",   "asset_type": "Stock"},
    "NVDA":  {"company_name": "NVIDIA Corporation",                "category": "Technology", "sector": "Technology",   "asset_type": "Stock"},
    "AMZN":  {"company_name": "Amazon.com Inc.",                   "category": "Technology", "sector": "Technology",   "asset_type": "Stock"},
    "GOOGL": {"company_name": "Alphabet Inc.",                     "category": "Technology", "sector": "Technology",   "asset_type": "Stock"},
    "JPM":   {"company_name": "JPMorgan Chase & Co.",              "category": "Financials", "sector": "Financials",   "asset_type": "Stock"},
    "GS":    {"company_name": "Goldman Sachs Group Inc.",          "category": "Financials", "sector": "Financials",   "asset_type": "Stock"},
    "BAC":   {"company_name": "Bank of America Corp.",             "category": "Financials", "sector": "Financials",   "asset_type": "Stock"},
    "MS":    {"company_name": "Morgan Stanley",                    "category": "Financials", "sector": "Financials",   "asset_type": "Stock"},
    "SPY":   {"company_name": "SPDR S&P 500 ETF Trust",            "category": "ETF",        "sector": "Broad Market", "asset_type": "ETF"},
    "QQQ":   {"company_name": "Invesco QQQ Trust",                 "category": "ETF",        "sector": "Technology",   "asset_type": "ETF"},
    "XLF":   {"company_name": "Financial Select Sector SPDR Fund", "category": "ETF",        "sector": "Financials",   "asset_type": "ETF"},
}


def get_engine():
    return create_engine(DATABASE_URL)


def load_ticker_metadata(engine):
    df = pd.DataFrame([{"ticker": t, **meta} for t, meta in TICKER_METADATA.items()])
    df.to_sql("ticker_metadata", engine, if_exists="replace", index=False)
    print(f"  [OK]  ticker_metadata       — {len(df)} rows")


def load_market_prices(engine):
    path = os.path.join(PROCESSED_DIR, "market_prices.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    df.to_sql("market_prices", engine, if_exists="replace", index=False, chunksize=1000)
    print(f"  [OK]  market_prices         — {len(df):,} rows")


def load_macro_indicators(engine):
    path = os.path.join(RAW_DIR, "macro_indicators_raw.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    df.to_sql("macro_indicators", engine, if_exists="replace", index=False, chunksize=1000)
    print(f"  [OK]  macro_indicators      — {len(df):,} rows")


def load_analytics_metrics(engine):
    path = os.path.join(PROCESSED_DIR, "analytics_metrics.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    df.to_sql("analytics_metrics", engine, if_exists="replace", index=False, chunksize=1000)
    print(f"  [OK]  analytics_metrics     — {len(df):,} rows")


def load_to_postgres():
    print("Connecting to PostgreSQL...")
    engine = get_engine()

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connection OK\n")

    print("Loading tables...")
    load_ticker_metadata(engine)
    load_market_prices(engine)
    load_macro_indicators(engine)
    load_analytics_metrics(engine)

    print("\nAll tables loaded successfully.")


if __name__ == "__main__":
    load_to_postgres()
