-- Count candles by symbol --
SELECT
    symbol,
    COUNT(*) as candle_count
FROM fact_price_ohlcv
GROUP BY symbol
ORDER BY candle_count DESC

-- Last loaded candle --
SELECT
    symbol,
    MAX(open_time) AS last_loaded

FROM raw_klines
GROUP BY symbol

-- Top price movements --
SELECT
    symbol,
    open_time,
    price_change_pct
FROM mart_top_movers
ORDER BY ABS(price_change_pct) DESC
LIMIT 20

-- Average volume --
SELECT
    symbol,
    ROUND(AVG(volume), 2) AS avg_volume
FROM fact_price_ohlcv
GROUP BY symbol

-- Maximum price --
SELECT
    symbol,
    MAX(high_price) AS max_price
FROM fact_price_ohlcv
GROUP BY symbol

-- RANK --
SELECT
    open_time,
    symbol,
    close_price,
    price_change_pct,
    RANK() OVER(
        PARTITION BY open_time
        ORDER BY ABS(price_change_pct) DESC
    ) AS movement_rank
FROM fact_price_ohlcv
ORDER BY open_time DESC, movement_rank

-- LAG --
SELECT
    symbol,
    open_time,
    close_price,
    LAG(close_price) OVER (
        PARTITION by symbol
        ORDER BY open_time
    ) AS previous_close_price,
    close_price - LAG(close_price) OVER(
        PARTITION by symbol
        ORDER BY open_time
    ) AS close_price_diff
FROM fact_price_ohlcv
ORDER BY symbol, open_time;

-- AVG --
SELECT
    symbol,
    open_time,
    close_price,
    AVF(close_price) OVER (
        PARTITION BY symbol
        ORDER BY open_time
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS moving_avg_5
FROM fact_price_ohlcv
ORDER BY symbol, open_time;

-- ROW_NUMBER --
SELECT
    symbol,
    open_time,
    close_price,
    volume
FROM (
    SELECT
        symbol,
        open_time,
        close_price,
        volume,
        ROW_NUMBER() OVER(
            PARTITION BY symbol
            ORDER BY open_time DESC
        ) AS rn
    FROM fact_price_ohlcv
) t
WHERE rn = 1
ORDER BY symbol;

 -- --
 SELECT
    symbol,
    open_time,
    close_price,

    LAG(close_price) OVER(
        PARTITION by symbol
        ORDER BY open_time
    ) AS  previous_close_price

    close_price - LAG(close_price) OVER(
        PARTITION BY symbol
        ORDER BY  open_time
    ) AS price_diff_from_previous,

    AVG(close_price) OVER (
        PARTITION BY symbol
        ORDER BY open_time
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS moving_avg_5

    RANK() OVER (
        PARTITION BY open_time
        ORDER BY ABS(price_change_pact) DESC
    ) AS movement_rank

FROM fact_price_ohlcv
ORDER BY open_time DESC, symbol;

