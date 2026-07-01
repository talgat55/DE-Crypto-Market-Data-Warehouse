from datetime import datetime
from db import get_connection
from extract import fetch_klines
from transform import load_fact_price_ohlcv
from marts import build_mart_top_movers, build_mart_coin_hourly
from quality import run_quality_checks

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
INTERVAL = "1h"

def ms_to_datetime(ms: int):
    return datetime.fromtimestamp(ms / 1000)

def save_klines(symbol: str, interval: str, klines: list):
    conn = get_connection()
    cur = conn.cursor()

    sql = """
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, interval, open_time)
        DO NOTHING;
    """

    inserted = 0

    for k in klines:
        cur.execute(sql, (
            symbol,
            interval,
            ms_to_datetime(k[0]),
            k[1],
            k[2],
            k[3],
            k[4],
            k[5],
            ms_to_datetime(k[6]),
        ))

        if cur.rowcount == 1:
            inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    return inserted

def main():
    for symbol in SYMBOLS:
        print(f"Fetching {symbol}...")

        klines = fetch_klines(symbol, INTERVAL, limit=100)
        inserted = save_klines(symbol, INTERVAL, klines)

    affected = load_fact_price_ohlcv()
    print(f"fact_price_ohlcv affected rows: {affected}")

    affected = load_fact_price_ohlcv()
    print(f"fact_price_ohlcv affected rows: {affected}")

    hourly_rows = build_mart_coin_hourly()
    print(f"mart_coin_hourly affected rows: {hourly_rows}")

    top_movers_rows = build_mart_top_movers()
    print(f"mart_top_movers affected rows: {top_movers_rows}")

    checks = run_quality_checks()
    print("Quantity checks:")
    for check in checks:
        print(f"{check['check']}: {check['status']}")

if __name__ == "__main__":
    main()