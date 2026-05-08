-- ============================================================
-- 1. Top 5 tickers by cumulative return
-- ============================================================
SELECT ticker, company_name, category, cumulative_return, return_rank
FROM vw_top_performers
ORDER BY return_rank
LIMIT 5;


-- ============================================================
-- 2. Bottom 5 tickers (worst performers)
-- ============================================================
SELECT ticker, company_name, category, cumulative_return, return_rank
FROM vw_top_performers
ORDER BY return_rank DESC
LIMIT 5;


-- ============================================================
-- 3. Most volatile tickers (90-day rolling vol)
-- ============================================================
SELECT ticker, company_name, category, rolling_vol_90, vol_rank
FROM vw_volatility_rankings
ORDER BY vol_rank
LIMIT 10;


-- ============================================================
-- 4. Monthly return trends by ticker
-- ============================================================
SELECT ticker, month, monthly_return, avg_daily_return, monthly_volatility, trading_days
FROM vw_monthly_returns
ORDER BY ticker, month;


-- ============================================================
-- 5. Sector performance comparison (latest date)
-- ============================================================
SELECT category, avg_cumulative_return, avg_daily_return, avg_vol_30, avg_vol_90
FROM vw_sector_performance
WHERE date = (SELECT MAX(date) FROM vw_sector_performance)
ORDER BY avg_cumulative_return DESC;


-- ============================================================
-- 6. Tech vs Financials head-to-head
-- ============================================================
SELECT
    category,
    ROUND(AVG(cumulative_return)::NUMERIC, 4)  AS avg_cumulative_return,
    ROUND(AVG(rolling_vol_90)::NUMERIC, 4)     AS avg_vol_90,
    ROUND(MIN(drawdown)::NUMERIC, 4)           AS worst_drawdown
FROM vw_latest_market_summary
WHERE category IN ('Technology', 'Financials')
GROUP BY category
ORDER BY avg_cumulative_return DESC;


-- ============================================================
-- 7. Largest drawdowns by ticker
-- ============================================================
SELECT ticker, company_name, category, max_drawdown, all_time_max_drawdown, avg_drawdown
FROM vw_drawdown_summary
ORDER BY max_drawdown ASC;


-- ============================================================
-- 8. Recent anomaly / volatility spike events (last 90 days)
-- ============================================================
SELECT date, ticker, company_name, daily_return, rolling_vol_30, volatility_z_score
FROM vw_anomaly_events
WHERE date >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY date DESC;


-- ============================================================
-- 9. Tickers with the most anomaly events (all time)
-- ============================================================
SELECT
    ticker,
    COUNT(*)                                      AS anomaly_count,
    ROUND(AVG(volatility_z_score)::NUMERIC, 4)   AS avg_z_score,
    ROUND(MAX(volatility_z_score)::NUMERIC, 4)   AS peak_z_score
FROM vw_anomaly_events
GROUP BY ticker
ORDER BY anomaly_count DESC;


-- ============================================================
-- 10. Best and worst month per ticker (all time)
-- ============================================================
SELECT DISTINCT ON (ticker)
    ticker, company_name, month, monthly_return
FROM vw_monthly_returns
ORDER BY ticker, monthly_return DESC;

SELECT DISTINCT ON (ticker)
    ticker, company_name, month, monthly_return
FROM vw_monthly_returns
ORDER BY ticker, monthly_return ASC;


-- ============================================================
-- 11. Correlation proxy — avg return by macro regime
--     (high vs low fed funds rate periods)
-- ============================================================
SELECT
    CASE WHEN mi.value >= 4 THEN 'High Rate (>=4%)' ELSE 'Low Rate (<4%)' END AS rate_regime,
    ROUND(AVG(am.daily_return)::NUMERIC, 6)     AS avg_daily_return,
    ROUND(STDDEV(am.daily_return)::NUMERIC, 6)  AS return_volatility,
    COUNT(*)                                     AS observations
FROM analytics_metrics am
JOIN macro_indicators mi
    ON mi.date = DATE_TRUNC('month', am.date)::DATE
    AND mi.indicator_name = 'Federal Funds Rate'
WHERE am.ticker = 'SPY'
GROUP BY rate_regime
ORDER BY rate_regime;


-- ============================================================
-- 12. Rolling 30-day vol trend for all tickers (last 6 months)
-- ============================================================
SELECT date, ticker, rolling_vol_30, volatility_z_score, anomaly_flag
FROM analytics_metrics
WHERE date >= CURRENT_DATE - INTERVAL '6 months'
ORDER BY ticker, date;
