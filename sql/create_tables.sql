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

CREATE TABLE IF NOT EXISTS fact_price_ohlcv (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    open_time TIMESTAMP NOT NULL,
    close_time TIMESTAMP,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume NUMERIC,
    price_change NUMERIC,
    price_change_pct NUMERIC,
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(symbol, interval, open_time)
);

CREATE TABLE IF NOT EXISTS mart_coin_hourly (
    symbol TEXT NOT  NULL,
    interval TEXT NOT  NULL,
    open_time TIMESTAMP NOT  NULL,
    close_price NUMERIC,
    volume NUMERIC,
    price_change_pct NUMERIC,
    create_at TIMESTAMP DEFAULT  NOW(),

    PRIMARY KEY(symbol, interval, open_time)
);

CREATE TABLE IF NOT EXISTS mart_top_movers (
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    open_time TIMESTAMP NOT NULL,
    close_price NUMERIC,
    price_change_pct NUMERIC,
    volume NUMERIC,
    rank_by_change INT,
    create_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (symbol, interval, open_time)
);

