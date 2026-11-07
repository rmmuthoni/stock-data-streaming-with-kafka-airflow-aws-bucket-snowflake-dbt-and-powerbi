from airflow.sdk import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def sample_task():
    print("This is a sample task.") 

def another_task():
    print("This is another task.")




default_args = {
    'owner': 'rmmuthoni@me.com',
    "retry_delay": timedelta(minutes=5),
    "retries": 3
}

with DAG(
    dag_id="sample_dag",
    default_args=default_args, 
    description="A sample DAG", 
    schedule=timedelta(seconds=30),
    start_date=datetime(2024, 6, 1), 
    catchup=False,
    tags=["sample", "test"]
) as dag: 
    task1 = PythonOperator(
        task_id="sample_task",
        python_callable=sample_task
    )

    task2 = PythonOperator(
        task_id="another_task",
        python_callable=another_task
    )

    task1 >> task2