from db import get_connection

def build_mart_coin_hourly():
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO mart_coin_hourly (
            symbol,
            interval,
            open_time,
            close_price,
            volume,
            price_change_pct
        )
        SELECT
            symbol,
            interval,
            open_time,
            close_price,
            volume,
            price_change_pct
        FROM fact_price_ohlcv
        ON CONFLICT (symbol, interval, open_time)
        DO UPDATE SET
            close_price = EXCLUDED.close_price,
            volume = EXCLUDED.volume,
            price_change_pct = EXCLUDED.price_change_pct;
    """

    cur.execute(sql)
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    return affected

def build_mart_top_movers():
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO mart_top_movers (
            symbol,
            interval,
            open_time,
            close_price,
            price_change_pct,
            volume,
            rank_by_change
        )
        SELECT
            symbol,
            interval,
            open_time,
            close_price,
            price_change_pct,
            volume,
            RANK() OVER (
                PARTITION BY open_time
                ORDER BY ABS(price_change_pct) DESC
            ) as rank_by_change
        FROM fact_price_ohlcv
        ON CONFLICT (symbol, interval, open_time)
        DO UPDATE SET
            close_price = EXCLUDED.close_price,
            price_change_pct = EXCLUDED.price_change_pct,
            volume = EXCLUDED.volume,
            rank_by_change = EXCLUDED.rank_by_change;
    """

    cur.execute(sql)
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    return affected