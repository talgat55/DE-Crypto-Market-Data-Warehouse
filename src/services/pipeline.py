from datetime import datetime
from db import get_connection

def start_pipeline_run():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO pipeline_runs (started_at, status)
        VALUES (%s, %s)
        RETURNING id
    """, (datetime.now(), "running"))

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
        error_message: str | None = None
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE pipeline_runs
        SET
            finished_at = %s,
            status = %s,
            raw_inserted_rows = %s,
            fact_affected_row = %s,
            mart_hourly_row = %s,
            mart_top_movers_rows = %s,
            error_message  = %s
        WHERE id = %s;    
    """, (
        datetime.now(),
        status,
        raw_inserted_rows,
        fact_affected_rows,
        mart_hourly_rows,
        mart_top_movers_rows,
        error_message,
        run_id
    ))

    conn.commit()
    cur.close()
    conn.close()

