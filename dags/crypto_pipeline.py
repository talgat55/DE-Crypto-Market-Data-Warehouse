from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from services.pipeline import run_pipeline

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
    run_crypto_pipeline = PythonOperator(
        task_id="run_crypto_pipeline",
        python_callable=run_pipeline
    )