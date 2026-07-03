INSERT INTO pipeline_runs (started_at, status)
VALUES (%s, %s)
RETURNING id;
