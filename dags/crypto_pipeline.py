from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from services.pipeline import (
    extract_raw,
    transform_fact,
    build_marts,
    quality_checks
)

default_args = {
    "owner": "user",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="crypto_market_pipeline",
    default_args=default_args,
    description="Crypto market ETL pipeline",
    start_date=datetime(2026,1,1),
    schedule_interval="@hourly",
    catchup=False,
    tags=["crypto", "etl", "data-engineering"]
) as dag:

    extract_raw_task = PythonOperator(
        task_id="extract_raw",
        python_callable=extract_raw
    )

    transform_fact_task = PythonOperator(
        task_id="transform_fact",
        python_callable=transform_fact
    )

    build_marts_task = PythonOperator(
        task_id="build_marts",
        python_callable=build_marts
    )

    quality_checks_task = PythonOperator(
        task_id="quality_checks",
        python_callable=quality_checks
    )

    extract_raw_task >> transform_fact_task >> build_marts_task >> quality_checks_task