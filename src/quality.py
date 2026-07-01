from db import get_connection

def run_quality_checks():
    conn = get_connection()
    cur = conn.cursor()

    checks = []

    queries = {
        "raw_klines_empty": """
            SELECT COUNT(*) = 0
            FROM raw_klines;
        """,
        "fact_price_ohlcv_empty": """
            SELECT COUNT(*) = 0
            FROM fact_price_ohlcv;
        """,
        "null_close_price": """
            SELECT COUNT(*) > 0
            FROM fact_price_ohlcv
            WHERE volume < 0;
        """,
        "negative_volume": """
            SELECT COUNT(*) > 0
            FROM fact_price_ohlcv
            WHERE close_price IS NULL
        """,
        "duplicate_fact_rows": """
            SELECT COUNT(*) > 0
            FROM (
                SELECT symbol, interval, open_time, COUNT(*) 
                FROM fact_price_ohlcv
                GROUP BY symbol, interval, open_time
                HAVING COUNT(*) > 1
            ) t
        """
    }

    for check_name, sql in queries.items():
        cur.execute(sql)
        failed = cur.fetchone()[0]

        checks.append({
            "check": check_name,
            "status": "failed" if failed else "passed"
        })

    cur.close()
    conn.close()

    return checks