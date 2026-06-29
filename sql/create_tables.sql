CREATE TABLE IF NOT EXISTS raw_klines (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    open_time TIMESTAMP NOT NULL,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume NUMERIC,
    close_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(symbol, interval, open_time)
);