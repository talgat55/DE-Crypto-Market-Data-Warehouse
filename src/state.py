from db import get_connection
from sql_loader import load_sql


def get_last_open_time_ms(symbol: str, interval: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(load_sql("get_last_open_time.sql"), (symbol, interval))

    last_open_time = cur.fetchone()[0]

    cur.close()
    conn.close()

    if last_open_time is None:
        return None

    return int(last_open_time.timestamp() * 1000)
