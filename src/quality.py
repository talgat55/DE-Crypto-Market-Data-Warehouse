from db import get_connection
from sql_loader import load_sql

QUALITY_CHECKS = [
    "raw_klines_empty",
    "fact_price_ohlcv_empty",
    "null_close_price",
    "negative_volume",
    "duplicate_fact_rows",
]


def run_quality_checks():
    conn = get_connection()
    cur = conn.cursor()

    checks = []

    for check_name in QUALITY_CHECKS:
        cur.execute(load_sql(f"quality/{check_name}.sql"))
        failed = cur.fetchone()[0]

        checks.append({
            "check": check_name,
            "status": "failed" if failed else "passed"
        })

    cur.close()
    conn.close()

    return checks
