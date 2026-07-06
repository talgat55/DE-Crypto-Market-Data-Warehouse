from datetime import datetime

from config import BINANCE_KLINES_LIMIT, KLINE_INTERVAL, KLINE_SYMBOLS
from db import get_connection
from extract import fetch_klines
from logger import get_logger
from marts import build_mart_coin_hourly, build_mart_top_movers
from quality import run_quality_checks
from state import get_last_open_time_ms
from sql_loader import load_sql
from transform import load_fact_price_ohlcv

logger = get_logger(__name__)


def ms_to_datetime(ms: int):
    return datetime.fromtimestamp(ms / 1000)


def save_klines(symbol: str, interval: str, klines: list):
    conn = get_connection()
    cur = conn.cursor()

    inserted = 0

    for k in klines:
        cur.execute(load_sql("insert_raw_klines.sql"), (
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


def start_pipeline_run():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(load_sql("insert_pipeline_run.sql"), (datetime.now(), "running"))

    run_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return run_id


def finish_pipeline_run(
    run_id: int,
    status: str,
    raw_inserted_rows: int = 0,
    fact_affected_rows: int = 0,
    mart_hourly_rows: int = 0,
    mart_top_movers_rows: int = 0,
    error_message: str | None = None,
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(load_sql("update_pipeline_run.sql"), (
        datetime.now(),
        status,
        raw_inserted_rows,
        fact_affected_rows,
        mart_hourly_rows,
        mart_top_movers_rows,
        error_message,
        run_id,
    ))

    conn.commit()
    cur.close()
    conn.close()

def extract_raw():
    total_raw_inserted = 0

    for symbol in KLINE_SYMBOLS:
        logger.info(f"Fetching {symbol}...")

        last_open_time_ms = get_last_open_time_ms(symbol,KLINE_INTERVAL)
        start_time_ms = None if last_open_time_ms is None else last_open_time_ms + 1
        klines = fetch_klines(
            symbol=symbol,
            interval = KLINE_INTERVAL,
            limit=BINANCE_KLINES_LIMIT,
            start_time_ms=start_time_ms
        )

        inserted = save_klines(symbol, KLINE_INTERVAL, klines)
        total_raw_inserted += inserted

        logger.info(f"{symbol}: inserted {inserted} rows")

    logger.info(f"Total raw inserted rows: {total_raw_inserted}")
    return  total_raw_inserted

def transform_fact():
    fact_rows = load_fact_price_ohlcv()
    logger.info(f"fact_price_ohlcv affected rows: {fact_rows}")
    return fact_rows

def build_marts():
    hourly_rows = build_mart_coin_hourly()
    logger.info(f"mart_coin_hourly affected rows: {hourly_rows}")

    top_movers_rows = build_mart_top_movers()
    logger.info(f"mart_top_movers affected rows: {top_movers_rows}")

    return {
        "mart_coin_hourly": hourly_rows,
        "mart_top_movers": top_movers_rows,
    }

def quality_checks():
    checks = run_quality_checks()

    logger.info("Quality checks:")
    for check in checks:
        logger.info(f"{check['check']}: {check['status']}")

    failed_checks = [c for c in checks if c["status"] == "failed"]

    if failed_checks:
        raise ValueError(f"Failed quality checks: {failed_checks}")



def run_pipeline():
    extract_raw()
    transform_fact()
    build_marts()
    quality_checks()