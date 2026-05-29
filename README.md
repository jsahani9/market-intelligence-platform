# Financial Market Intelligence & Risk Analytics Platform

An end-to-end financial analytics platform built with Python, PostgreSQL, SQL, and Power BI. It ingests 5 years of real market and macroeconomic data, computes institutional-grade risk and performance metrics, stores analytical datasets in PostgreSQL, and visualizes market performance, volatility, drawdowns, and sector trends through an executive-style dashboard.

---

## Business Problem

Financial analysts need a structured way to monitor equity performance, identify risk events, and understand how macroeconomic conditions relate to market behavior. Most tools either require expensive subscriptions or lack the depth needed for proper risk analysis. This platform solves that by building a full analytics pipeline from raw data to interactive dashboards — entirely with open-source tools.

---

## Project Objective

- Pull 5 years of daily market data for 12 tickers across Technology, Financials, and ETFs
- Compute key risk and performance metrics: returns, volatility, drawdowns, moving averages, anomaly flags
- Store all data in a structured PostgreSQL database with analytical SQL views
- Visualize insights through a 3-page Power BI dashboard
- Provide exploratory analysis through 5 Jupyter notebooks

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data Extraction | Python, yfinance, FRED API |
| Data Processing | pandas, numpy |
| Database | PostgreSQL |
| SQL Analytics | PostgreSQL views and queries |
| Notebooks | Jupyter, matplotlib |
| Dashboard | Power BI (web) |
| Version Control | Git, GitHub |

---

## Data Sources

| Source | Data |
|---|---|
| [yfinance](https://github.com/ranaroussi/yfinance) | Daily OHLCV + adjusted close for 12 tickers (2021–2026) |
| [FRED API](https://fred.stlouisfed.org/) | Federal Funds Rate, 10-Year Treasury Yield, CPI, Unemployment Rate |

### Ticker Universe

| Category | Tickers |
|---|---|
| Technology | AAPL, MSFT, NVDA, AMZN, GOOGL |
| Financials | JPM, GS, BAC, MS |
| ETFs / Benchmarks | SPY, QQQ, XLF |

---

## Project Structure

```
market-intelligence-platform/
├── data/
│   ├── raw/                    # Raw CSV files from yfinance and FRED
│   ├── processed/              # Cleaned and transformed data
│   └── exports/                # Power BI ready exports
├── notebooks/
│   ├── 01_eda_market_data.ipynb
│   ├── 02_analytics_metrics.ipynb
│   ├── 03_sector_analysis.ipynb
│   ├── 04_macro_relationships.ipynb
│   └── 05_anomaly_detection.ipynb
├── scripts/
│   ├── extract_market_data.py  # Pull OHLCV data from yfinance
│   ├── extract_macro_data.py   # Pull macro indicators from FRED
│   ├── transform_market_data.py # Compute all analytics metrics
│   ├── load_to_postgres.py     # Load data into PostgreSQL
│   └── run_pipeline.py         # End-to-end pipeline runner
├── sql/
│   ├── schema.sql              # Table definitions and indexes
│   ├── analytics_views.sql     # 7 analytical SQL views
│   └── analysis_queries.sql    # 12 business analysis queries
├── docs/
│   └── screenshots/            # Power BI dashboard screenshots
├── .env.example
├── requirements.txt
└── README.md
```

---

## Database Schema

### `market_prices`
Daily OHLCV data for all tickers.
`date, ticker, open, high, low, close, adj_close, volume, category`

### `analytics_metrics`
Computed risk and performance metrics per ticker per day.
`date, ticker, daily_return, cumulative_return, rolling_vol_30/60/90, moving_avg_50/200, drawdown, max_drawdown_to_date, volatility_z_score, anomaly_flag`

### `macro_indicators`
FRED macroeconomic time series.
`date, indicator_name, series_id, value`

### `ticker_metadata`
Static metadata for each ticker.
`ticker, company_name, category, sector, asset_type`

---

## Key Metrics Calculated

| Metric | Description |
|---|---|
| Daily Return | Percentage change in adjusted close price |
| Cumulative Return | Total return from start of period |
| Rolling Volatility (30/60/90d) | Annualised standard deviation of daily returns |
| Moving Average (50/200d) | Trend indicators on adjusted close |
| Drawdown | Percentage decline from rolling peak |
| Max Drawdown to Date | Worst drawdown seen up to each date |
| Volatility Z-Score | Standard deviations from rolling mean volatility |
| Anomaly Flag | 1 when volatility z-score exceeds ±2 |

---

## SQL Views

| View | Purpose |
|---|---|
| `vw_latest_market_summary` | Snapshot of all tickers on the latest trading day |
| `vw_top_performers` | Tickers ranked by cumulative return |
| `vw_volatility_rankings` | Tickers ranked by 90-day rolling volatility |
| `vw_monthly_returns` | Month-by-month return aggregation |
| `vw_sector_performance` | Category-level performance over time |
| `vw_anomaly_events` | All dates where volatility z-score exceeded ±2 |
| `vw_drawdown_summary` | Max and average drawdown per ticker |

---

## Power BI Dashboard

### Page 1 — Market Overview
- KPI cards: best cumulative return, max volatility, worst drawdown
- ETF price trend (SPY, QQQ, XLF)
- Cumulative return ranking by ticker
- Date range slicer

### Page 2 — Risk Analysis
- Rolling 30-day volatility for all tickers
- 90-day volatility ranking
- Drawdown trends
- Anomaly event count by ticker

### Page 3 — Stock Deep Dive
- Ticker slicer
- Price + moving average trend
- Cumulative return over time
- Drawdown and rolling volatility

---

## Sample Insights

- **NVDA** delivered the highest 5-year cumulative return at **1,257%**, significantly outperforming all other tickers
- **NVDA** also had the highest 90-day rolling volatility at **34.8%** — high reward came with high risk
- **BAC** and **AMZN** were the weakest performers with cumulative returns under **55%**
- Volatility spiked across all tickers in **2022** during the Fed rate hiking cycle and in **2025** during market uncertainty
- **Financials** (GS, MS, JPM) showed strong cumulative returns while maintaining moderate volatility compared to tech stocks
- **SPY** and **QQQ** confirm the broad market trend — QQQ outperforming SPY due to tech concentration

---

## How to Run the Pipeline

### 1. Setup

```bash
git clone https://github.com/jsahani9/market-intelligence-platform.git
cd market-intelligence-platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials and FRED API key
```

### 3. Create the database

```bash
psql -U postgres -c "CREATE DATABASE market_intelligence;"
```

### 4. Run the full pipeline

```bash
python scripts/run_pipeline.py
```

### 5. Set up SQL views

```bash
psql -U postgres -d market_intelligence -f sql/analytics_views.sql
```

### 6. Run analysis queries

```bash
psql -U postgres -d market_intelligence -f sql/analysis_queries.sql
```

---

## Future Improvements

- Add real-time data refresh via scheduled pipeline
- Expand ticker universe to include international markets
- Add Sharpe ratio and beta calculations
- Build a Streamlit web app as an alternative to Power BI
- Add sector rotation analysis
- Integrate options data for implied volatility comparison

---

## Author

**Jasveen Sahani**
[GitHub](https://github.com/jsahani9)
