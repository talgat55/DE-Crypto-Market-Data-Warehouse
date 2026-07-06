INSERT INTO raw_klines (
    symbol,
    interval,
    open_time,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    close_time
)
VALUES %s
ON CONFLICT (symbol, interval, open_time)
DO NOTHING;
