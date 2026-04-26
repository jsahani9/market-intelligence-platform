import os
import requests
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY", "")

MACRO_INDICATORS = {
    "FEDFUNDS": "Federal Funds Rate",
    "DGS10":    "10-Year Treasury Yield",
    "CPIAUCSL": "CPI (Inflation Proxy)",
    "UNRATE":   "Unemployment Rate",
}

END_DATE   = date.today().isoformat()
START_DATE = (date.today() - timedelta(days=5 * 365)).isoformat()

OUTPUT_PATH = os.path.join("data", "raw", "macro_indicators_raw.csv")

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_series(series_id: str, name: str) -> pd.DataFrame:
    params = {
        "series_id":          series_id,
        "observation_start":  START_DATE,
        "observation_end":    END_DATE,
        "api_key":            FRED_API_KEY,
        "file_type":          "json",
    }
    resp = requests.get(FRED_URL, params=params, timeout=15)
    resp.raise_for_status()

    observations = resp.json().get("observations", [])
    df = pd.DataFrame(observations)[["date", "value"]]
    df["date"]           = pd.to_datetime(df["date"]).dt.date
    df["value"]          = pd.to_numeric(df["value"], errors="coerce")
    df["indicator_name"] = name
    df["series_id"]      = series_id
    df.dropna(subset=["value"], inplace=True)
    return df[["date", "indicator_name", "series_id", "value"]]


def extract_macro_data() -> pd.DataFrame:
    if not FRED_API_KEY:
        raise EnvironmentError(
            "FRED_API_KEY not set. Get a free key at https://fred.stlouisfed.org/docs/api/api_key.html "
            "and add it to your .env file."
        )

    print(f"Pulling macro data from FRED: {START_DATE} → {END_DATE}\n")

    frames = []
    for series_id, name in MACRO_INDICATORS.items():
        try:
            df = fetch_series(series_id, name)
            frames.append(df)
            print(f"  [OK]    {name} ({series_id}): {len(df):,} rows")
        except Exception as exc:
            print(f"  [ERROR] {name} ({series_id}): {exc}")

    if not frames:
        raise RuntimeError("No macro data fetched. Check your API key or internet connection.")

    combined = pd.concat(frames, ignore_index=True)
    combined.sort_values(["indicator_name", "date"], inplace=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    combined.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved {len(combined):,} rows → {OUTPUT_PATH}")
    print(f"Indicators: {combined['indicator_name'].nunique()} | Date range: {combined['date'].min()} to {combined['date'].max()}")
    return combined


if __name__ == "__main__":
    extract_macro_data()
