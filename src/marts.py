from db import get_connection
from sql_loader import load_sql


def build_mart_coin_hourly():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(load_sql("build_mart_coin_hourly.sql"))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    return affected


def build_mart_top_movers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(load_sql("build_mart_top_movers.sql"))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    return affected
