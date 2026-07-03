INSERT INTO fact_price_ohlcv (
    symbol,
    interval,
    open_time,
    close_time,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    price_change,
    price_change_pct
)
SELECT
    symbol,
    interval,
    open_time,
    close_time,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    close_price - open_price AS price_change,
    CASE
        WHEN open_price = 0 THEN NULL
        ELSE ROUND(((close_price - open_price) / open_price) * 100, 4)
    END AS price_change_pct
FROM raw_klines
ON CONFLICT (symbol, interval, open_time)
DO UPDATE SET
    close_time = EXCLUDED.close_time,
    open_price = EXCLUDED.open_price,
    high_price = EXCLUDED.high_price,
    low_price = EXCLUDED.low_price,
    close_price = EXCLUDED.close_price,
    volume = EXCLUDED.volume,
    price_change = EXCLUDED.price_change,
    price_change_pct = EXCLUDED.price_change_pct;
