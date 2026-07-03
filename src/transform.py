from db import get_connection
from sql_loader import load_sql


def load_fact_price_ohlcv():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(load_sql("load_fact_price_ohlcv.sql"))
    affected = cur.rowcount

    conn.commit()
    cur.close()
    conn.close()

    return affected
