INSERT INTO mart_top_movers (
    symbol,
    interval,
    open_time,
    close_price,
    price_change_pct,
    volume,
    rank_by_change
)
SELECT
    symbol,
    interval,
    open_time,
    close_price,
    price_change_pct,
    volume,
    RANK() OVER (
        PARTITION BY open_time
        ORDER BY ABS(price_change_pct) DESC
    ) as rank_by_change
FROM fact_price_ohlcv
ON CONFLICT (symbol, interval, open_time)
DO UPDATE SET
    close_price = EXCLUDED.close_price,
    price_change_pct = EXCLUDED.price_change_pct,
    volume = EXCLUDED.volume,
    rank_by_change = EXCLUDED.rank_by_change;
