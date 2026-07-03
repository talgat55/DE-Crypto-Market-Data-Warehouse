SELECT COUNT(*) > 0
FROM fact_price_ohlcv
WHERE close_price IS NULL;
