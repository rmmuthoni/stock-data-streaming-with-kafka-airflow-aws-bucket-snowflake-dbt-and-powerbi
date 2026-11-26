# from pathlib import Path 
# import sys 

# from airflow.sdk import DAG 
# from airflow.operators.python import PythonOperator

# from datetime import datetime, timedelta

# # HOME Path 
# AIRFLOW_HOME = Path("/opt/airflow") 
# if str(AIRFLOW_HOME) not in sys.path:
#     sys.path.insert(0, str(AIRFLOW_HOME))

# from scripts.fetch_company_financials import save_financials_to_file

# def sample_task():
#     print("This is a sample task")

# # DAG configuration
# default_args = {
#     'owner': 'rmmuthoni@me.com',
#     "retry_delay": timedelta(seconds=10),
#     "retries": 3
# }

# with DAG(
#     dag_id="fetch_company_financials",
#     default_args=default_args, 
#     description="Fetches company financials and saves to JSON files", 
#     schedule=timedelta(hours=24),
#     start_date=datetime(2024, 6, 1), 
#     catchup=False,
#     tags=["financials", "company", "data"]
# ) as dag: 

    
#     task_fetch_company_financials = PythonOperator(
#         task_id="fetch_company_financials",
#         python_callable=sample_task
#     )

   