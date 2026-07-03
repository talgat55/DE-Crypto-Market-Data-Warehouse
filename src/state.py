from db import get_connection

def get_last_open_time_ms(symbol: str, interval: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(open_time)
        FROM raw_klines
        WHERE symbol = %s AND interval = %s;
    """, (symbol, interval))

    last_open_time = cur.fetchone()[0]

    cur.close()
    conn.close()

    if last_open_time is None:
        return None

    return int(last_open_time.timestamp() * 1000)

