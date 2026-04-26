import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     os.getenv("DB_PORT", "5432"),
    "name":     os.getenv("DB_NAME", "market_intelligence"),
}

DATABASE_URL = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['name']}"
)

TICKERS = {
    "Technology": ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"],
    "Financials":  ["JPM", "GS", "BAC", "MS"],
    "ETF":         ["SPY", "QQQ", "XLF"],
}

TICKER_METADATA = {
    "AAPL":  {"company_name": "Apple Inc.",                       "category": "Technology", "sector": "Technology", "asset_type": "Stock"},
    "MSFT":  {"company_name": "Microsoft Corporation",            "category": "Technology", "sector": "Technology", "asset_type": "Stock"},
    "NVDA":  {"company_name": "NVIDIA Corporation",               "category": "Technology", "sector": "Technology", "asset_type": "Stock"},
    "AMZN":  {"company_name": "Amazon.com Inc.",                  "category": "Technology", "sector": "Technology", "asset_type": "Stock"},
    "GOOGL": {"company_name": "Alphabet Inc.",                    "category": "Technology", "sector": "Technology", "asset_type": "Stock"},
    "JPM":   {"company_name": "JPMorgan Chase & Co.",             "category": "Financials", "sector": "Financials", "asset_type": "Stock"},
    "GS":    {"company_name": "Goldman Sachs Group Inc.",         "category": "Financials", "sector": "Financials", "asset_type": "Stock"},
    "BAC":   {"company_name": "Bank of America Corp.",            "category": "Financials", "sector": "Financials", "asset_type": "Stock"},
    "MS":    {"company_name": "Morgan Stanley",                   "category": "Financials", "sector": "Financials", "asset_type": "Stock"},
    "SPY":   {"company_name": "SPDR S&P 500 ETF Trust",           "category": "ETF",        "sector": "Broad Market", "asset_type": "ETF"},
    "QQQ":   {"company_name": "Invesco QQQ Trust",                "category": "ETF",        "sector": "Technology",   "asset_type": "ETF"},
    "XLF":   {"company_name": "Financial Select Sector SPDR Fund","category": "ETF",        "sector": "Financials",   "asset_type": "ETF"},
}

ALL_TICKERS = [t for tickers in TICKERS.values() for t in tickers]

START_DATE = "2020-01-01"
END_DATE   = "2025-01-01"

MACRO_INDICATORS = {
    "FEDFUNDS": "Federal Funds Rate",
    "DGS10":    "10-Year Treasury Yield",
    "CPIAUCSL": "CPI (Inflation Proxy)",
    "UNRATE":   "Unemployment Rate",
}

DATA_RAW_DIR       = "data/raw"
DATA_PROCESSED_DIR = "data/processed"
DATA_EXPORTS_DIR   = "data/exports"
