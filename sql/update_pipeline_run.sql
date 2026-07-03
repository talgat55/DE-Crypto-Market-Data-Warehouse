UPDATE pipeline_runs
SET
    finished_at = %s,
    status = %s,
    raw_inserted_rows = %s,
    fact_affected_row = %s,
    mart_hourly_row = %s,
    mart_top_movers_rows = %s,
    error_message = %s
WHERE id = %s;
