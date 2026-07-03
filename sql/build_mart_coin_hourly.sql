INSERT INTO mart_coin_hourly (
    symbol,
    interval,
    open_time,
    close_price,
    volume,
    price_change_pct
)
SELECT
    symbol,
    interval,
    open_time,
    close_price,
    volume,
    price_change_pct
FROM fact_price_ohlcv
ON CONFLICT (symbol, interval, open_time)
DO UPDATE SET
    close_price = EXCLUDED.close_price,
    volume = EXCLUDED.volume,
    price_change_pct = EXCLUDED.price_change_pct;
