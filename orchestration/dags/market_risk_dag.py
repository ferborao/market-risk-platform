from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_ROOT = "/home/fernando/market-risk-platform"
VENV = f"{PROJECT_ROOT}/.venv/bin/activate"

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="market_risk_pipeline",
    description="Market risk calculation pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="0 8 * * 1-5",
    catchup=False,
    tags=["market_risk", "data-engineering"],
) as dag:

    download = BashOperator(
        task_id="download",
        bash_command=f"cd {PROJECT_ROOT} && source {VENV} && python ingestion/download.py",
    )

    validate = BashOperator(
        task_id="validate",
        bash_command=f"cd {PROJECT_ROOT} && source {VENV} && python ingestion/validate.py",
    )

    processing = BashOperator(
        task_id="processing",
        bash_command=f"cd {PROJECT_ROOT} && source {VENV} && python processing/returns.py && python processing/metrics.py && python processing/correlations.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT_ROOT}/market_risk_dbt && source {VENV} && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {PROJECT_ROOT}/market_risk_dbt && source {VENV} && dbt test",
    )

    download >> validate >> processing >> dbt_run >> dbt_test