SELECT COUNT(*) > 0
FROM (
    SELECT symbol, interval, open_time, COUNT(*)
    FROM fact_price_ohlcv
    GROUP BY symbol, interval, open_time
    HAVING COUNT(*) > 1
) t;
