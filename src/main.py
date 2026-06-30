from datetime import datetime
from db import get_connection
from extract import fetch_klines

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

        print(f"{symbol}: inserted {inserted}  rows")

if __name__ == "__main__":
    main()