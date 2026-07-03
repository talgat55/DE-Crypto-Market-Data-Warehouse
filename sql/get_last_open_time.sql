SELECT MAX(open_time)
FROM raw_klines
WHERE symbol = %s AND interval = %s;
