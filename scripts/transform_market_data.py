import os
import pandas as pd
import numpy as np

INPUT_PATH       = os.path.join("data", "raw", "market_prices_raw.csv")
PROCESSED_DIR    = os.path.join("data", "processed")
PRICES_OUT       = os.path.join(PROCESSED_DIR, "market_prices.csv")
ANALYTICS_OUT    = os.path.join(PROCESSED_DIR, "analytics_metrics.csv")


def compute_metrics(group: pd.DataFrame) -> pd.DataFrame:
    g = group.sort_values("date").copy()

    # Returns
    g["daily_return"]       = g["adj_close"].pct_change()
    g["cumulative_return"]  = (1 + g["daily_return"]).cumprod() - 1

    # Rolling volatility — annualised
    g["rolling_vol_30"]  = g["daily_return"].rolling(30).std()  * np.sqrt(252)
    g["rolling_vol_60"]  = g["daily_return"].rolling(60).std()  * np.sqrt(252)
    g["rolling_vol_90"]  = g["daily_return"].rolling(90).std()  * np.sqrt(252)

    # Moving averages
    g["moving_avg_50"]   = g["adj_close"].rolling(50).mean()
    g["moving_avg_200"]  = g["adj_close"].rolling(200).mean()

    # Drawdown
    rolling_max               = g["adj_close"].cummax()
    g["drawdown"]             = (g["adj_close"] - rolling_max) / rolling_max
    g["max_drawdown_to_date"] = g["drawdown"].cummin()

    # Volatility z-score (30d vol normalised over trailing 90-day window)
    vol_mean                  = g["rolling_vol_30"].rolling(90).mean()
    vol_std                   = g["rolling_vol_30"].rolling(90).std()
    g["volatility_z_score"]   = (g["rolling_vol_30"] - vol_mean) / vol_std

    # Anomaly flag: z-score beyond ±2
    g["anomaly_flag"] = (g["volatility_z_score"].abs() > 2).astype(int)

    return g


def transform_market_data():
    print(f"Loading raw data from {INPUT_PATH}...")
    df = pd.read_csv(INPUT_PATH, parse_dates=["date"])
    print(f"  {len(df):,} rows | {df['ticker'].nunique()} tickers\n")

    print("Computing analytics metrics per ticker...")
    results = []
    for ticker, group in df.groupby("ticker"):
        metrics = compute_metrics(group)
        results.append(metrics)
        print(f"  [OK]  {ticker}: {len(metrics):,} rows")

    full = pd.concat(results, ignore_index=True)
    full.sort_values(["ticker", "date"], inplace=True)

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Clean market prices
    price_cols = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume", "category"]
    full[price_cols].to_csv(PRICES_OUT, index=False)
    print(f"\nSaved market_prices.csv       → {PRICES_OUT}")

    # Analytics metrics
    metric_cols = [
        "date", "ticker",
        "daily_return", "cumulative_return",
        "rolling_vol_30", "rolling_vol_60", "rolling_vol_90",
        "moving_avg_50", "moving_avg_200",
        "drawdown", "max_drawdown_to_date",
        "volatility_z_score", "anomaly_flag",
    ]
    full[metric_cols].to_csv(ANALYTICS_OUT, index=False)
    print(f"Saved analytics_metrics.csv   → {ANALYTICS_OUT}")

    print(f"\nDone. {len(full):,} total rows processed.")
    return full[price_cols], full[metric_cols]


if __name__ == "__main__":
    transform_market_data()
