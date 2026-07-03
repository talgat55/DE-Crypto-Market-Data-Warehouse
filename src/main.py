from datetime import datetime
from db import get_connection
from extract import fetch_klines
from transform import load_fact_price_ohlcv
from marts import build_mart_top_movers, build_mart_coin_hourly
from quality import run_quality_checks
from pipeline_runs import start_pipeline_run, finish_pipeline_run
from state import get_last_open_time_ms
from logger import get_logger

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
INTERVAL = "1h"

logger = get_logger(__name__)

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
    run_id = start_pipeline_run()
    total_raw_inserted = 0
    fact_rows = 0
    hourly_rows = 0
    top_movers_rows = 0

    try:
        for symbol in SYMBOLS:
            logger.info(f"Fetching {symbol}...")

            last_open_time_ms = get_last_open_time_ms(symbol, INTERVAL)

            if last_open_time_ms is None:
                start_time_ms = None
            else:
                start_time_ms = last_open_time_ms + 1

            klines = fetch_klines(
                symbol=symbol,
                interval=INTERVAL,
                limit=100,
                start_time_ms=start_time_ms
            )
            inserted = save_klines(symbol, INTERVAL, klines)
            total_raw_inserted += inserted

            logger.info(f"{symbol}: inserted {inserted} rows")

        fact_rows = load_fact_price_ohlcv()
        logger.info(f"fact_price_ohlcv affected rows: {fact_rows}")

        hourly_rows = build_mart_coin_hourly()
        logger.info(f"fact_price_ohlcv affected rows: {hourly_rows}")

        top_movers_rows = build_mart_top_movers()
        logger.info(f"mart_top_movers affected rows: {top_movers_rows}")
        checks = run_quality_checks()

        logger.info("Quality checks:")
        for check in checks:
            logger.info(f"{check['check']}: {check['status']}")

        failed_checks = [c for c in checks if c["status"] == "failed"]

        if failed_checks:
            finish_pipeline_run(
                run_id=run_id,
                status="failed",
                raw_inserted_rows=total_raw_inserted,
                fact_affected_rows=fact_rows,
                mart_hourly_rows=hourly_rows,
                mart_top_movers_rows=top_movers_rows,
                error_message=f"Failed checks: {failed_checks}"
            )
        else:
            finish_pipeline_run(
                run_id=run_id,
                status="success",
                raw_inserted_rows=total_raw_inserted,
                fact_affected_rows=fact_rows,
                mart_hourly_rows=hourly_rows,
                mart_top_movers_rows=top_movers_rows
            )

    except Exception as e:
        logger.exception("Pipeline failed")
        finish_pipeline_run(
            run_id=run_id,
            status="failed",
            raw_inserted_rows=total_raw_inserted,
            fact_affected_rows=fact_rows,
            mart_hourly_rows=hourly_rows,
            mart_top_movers_rows=top_movers_rows,
            error_message=str(e)
        )
        raise

if __name__ == "__main__":
    main()