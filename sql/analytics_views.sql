-- ============================================================
-- Latest snapshot per ticker (most recent trading day)
-- ============================================================
CREATE OR REPLACE VIEW vw_latest_market_summary AS
SELECT
    mp.ticker,
    tm.company_name,
    tm.category,
    tm.sector,
    tm.asset_type,
    mp.date,
    mp.close,
    mp.adj_close,
    mp.volume,
    am.daily_return,
    am.cumulative_return,
    am.rolling_vol_30,
    am.rolling_vol_90,
    am.drawdown,
    am.anomaly_flag
FROM market_prices mp
JOIN analytics_metrics am ON mp.date = am.date AND mp.ticker = am.ticker
JOIN ticker_metadata   tm ON mp.ticker = tm.ticker
WHERE mp.date = (SELECT MAX(date) FROM market_prices WHERE ticker = mp.ticker);


-- ============================================================
-- Top performers ranked by cumulative return (latest date)
-- ============================================================
CREATE OR REPLACE VIEW vw_top_performers AS
SELECT
    am.ticker,
    tm.company_name,
    tm.category,
    am.date,
    ROUND(am.cumulative_return::NUMERIC, 4)  AS cumulative_return,
    ROUND(am.daily_return::NUMERIC, 4)       AS daily_return,
    ROUND(am.rolling_vol_30::NUMERIC, 4)     AS rolling_vol_30,
    RANK() OVER (ORDER BY am.cumulative_return DESC) AS return_rank
FROM analytics_metrics am
JOIN ticker_metadata tm ON am.ticker = tm.ticker
WHERE am.date = (SELECT MAX(date) FROM analytics_metrics);


-- ============================================================
-- Volatility rankings (latest date)
-- ============================================================
CREATE OR REPLACE VIEW vw_volatility_rankings AS
SELECT
    am.ticker,
    tm.company_name,
    tm.category,
    am.date,
    ROUND(am.rolling_vol_30::NUMERIC, 4)      AS rolling_vol_30,
    ROUND(am.rolling_vol_60::NUMERIC, 4)      AS rolling_vol_60,
    ROUND(am.rolling_vol_90::NUMERIC, 4)      AS rolling_vol_90,
    ROUND(am.volatility_z_score::NUMERIC, 4)  AS volatility_z_score,
    RANK() OVER (ORDER BY am.rolling_vol_90 DESC NULLS LAST) AS vol_rank
FROM analytics_metrics am
JOIN ticker_metadata tm ON am.ticker = tm.ticker
WHERE am.date = (SELECT MAX(date) FROM analytics_metrics);


-- ============================================================
-- Monthly returns per ticker
-- ============================================================
CREATE OR REPLACE VIEW vw_monthly_returns AS
SELECT
    am.ticker,
    tm.company_name,
    tm.category,
    DATE_TRUNC('month', am.date)::DATE              AS month,
    ROUND(SUM(am.daily_return)::NUMERIC, 4)         AS monthly_return,
    ROUND(AVG(am.daily_return)::NUMERIC, 6)         AS avg_daily_return,
    ROUND(STDDEV(am.daily_return)::NUMERIC, 6)      AS monthly_volatility,
    COUNT(*)                                         AS trading_days
FROM analytics_metrics am
JOIN ticker_metadata tm ON am.ticker = tm.ticker
GROUP BY am.ticker, tm.company_name, tm.category, DATE_TRUNC('month', am.date)
ORDER BY am.ticker, month;


-- ============================================================
-- Sector / category performance over time
-- ============================================================
CREATE OR REPLACE VIEW vw_sector_performance AS
SELECT
    tm.category,
    am.date,
    ROUND(AVG(am.cumulative_return)::NUMERIC, 4)  AS avg_cumulative_return,
    ROUND(AVG(am.daily_return)::NUMERIC, 6)       AS avg_daily_return,
    ROUND(AVG(am.rolling_vol_30)::NUMERIC, 4)     AS avg_vol_30,
    ROUND(AVG(am.rolling_vol_90)::NUMERIC, 4)     AS avg_vol_90,
    COUNT(DISTINCT am.ticker)                      AS ticker_count
FROM analytics_metrics am
JOIN ticker_metadata tm ON am.ticker = tm.ticker
GROUP BY tm.category, am.date
ORDER BY am.date, tm.category;


-- ============================================================
-- Anomaly / volatility spike events
-- ============================================================
CREATE OR REPLACE VIEW vw_anomaly_events AS
SELECT
    am.date,
    am.ticker,
    tm.company_name,
    tm.category,
    ROUND(am.daily_return::NUMERIC, 4)            AS daily_return,
    ROUND(am.rolling_vol_30::NUMERIC, 4)          AS rolling_vol_30,
    ROUND(am.volatility_z_score::NUMERIC, 4)      AS volatility_z_score,
    am.anomaly_flag
FROM analytics_metrics am
JOIN ticker_metadata tm ON am.ticker = tm.ticker
WHERE am.anomaly_flag = 1
ORDER BY am.date DESC, am.volatility_z_score DESC;


-- ============================================================
-- Drawdown summary per ticker (worst & average)
-- ============================================================
CREATE OR REPLACE VIEW vw_drawdown_summary AS
SELECT
    am.ticker,
    tm.company_name,
    tm.category,
    ROUND(MIN(am.drawdown)::NUMERIC, 4)             AS max_drawdown,
    ROUND(MIN(am.max_drawdown_to_date)::NUMERIC, 4) AS all_time_max_drawdown,
    ROUND(AVG(am.drawdown)::NUMERIC, 4)             AS avg_drawdown,
    MAX(am.date)                                     AS as_of_date
FROM analytics_metrics am
JOIN ticker_metadata tm ON am.ticker = tm.ticker
GROUP BY am.ticker, tm.company_name, tm.category
ORDER BY max_drawdown ASC;
