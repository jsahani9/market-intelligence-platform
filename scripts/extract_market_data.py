import os
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

TICKERS = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL",
    "JPM", "GS", "BAC", "MS",
    "SPY", "QQQ", "XLF"
]

CATEGORY_MAP = {
    "AAPL": "Technology", "MSFT": "Technology", "NVDA": "Technology",
    "AMZN": "Technology", "GOOGL": "Technology",
    "JPM":  "Financials", "GS":   "Financials", "BAC":  "Financials", "MS": "Financials",
    "SPY":  "ETF",        "QQQ":  "ETF",        "XLF":  "ETF",
}

END_DATE   = date.today().isoformat()
START_DATE = (date.today() - timedelta(days=5 * 365)).isoformat()

OUTPUT_PATH = os.path.join("data", "raw", "market_prices_raw.csv")


def extract_market_data() -> pd.DataFrame:
    print(f"Pulling market data: {START_DATE} → {END_DATE}\n")

    frames = []

    for ticker in TICKERS:
        try:
            raw = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=False, progress=False)

            if raw.empty:
                print(f"  [WARN]  {ticker}: no data returned")
                continue

            # Reset index first so Date joins columns, then flatten any MultiIndex
            df = raw.reset_index()
            df.columns = [
                col[0].lower().replace(" ", "_") if isinstance(col, tuple) else col.lower().replace(" ", "_")
                for col in df.columns
            ]
            df["date"] = pd.to_datetime(df["date"]).dt.date

            df["ticker"]   = ticker
            df["category"] = CATEGORY_MAP[ticker]

            df = df[["date", "ticker", "open", "high", "low", "close", "adj_close", "volume", "category"]]
            frames.append(df)
            print(f"  [OK]    {ticker}: {len(df):,} rows")

        except Exception as exc:
            print(f"  [ERROR] {ticker}: {exc}")

    if not frames:
        raise RuntimeError("No data was fetched. Check your internet connection or ticker symbols.")

    combined = pd.concat(frames, ignore_index=True)
    combined.sort_values(["ticker", "date"], inplace=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    combined.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved {len(combined):,} rows → {OUTPUT_PATH}")
    print(f"Tickers: {combined['ticker'].nunique()} | Date range: {combined['date'].min()} to {combined['date'].max()}")
    return combined


if __name__ == "__main__":
    extract_market_data()
