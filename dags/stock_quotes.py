from pathlib import Path 
import sys 

from airflow.sdk import DAG 
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from datetime import datetime, timedelta

# HOME Path 
AIRFLOW_HOME = Path("/opt/airflow") 
if str(AIRFLOW_HOME) not in sys.path:
    sys.path.insert(0, str(AIRFLOW_HOME))

from scripts.download_s3_json_data import download_json_from_s3
from scripts.upload_s3_json_data_to_snowflake import upload_s3_json_data_to_snowflake


# DAG configuration
default_args = {
    'owner': 'rmmuthoni@me.com',
    "retry_delay": timedelta(seconds=10),
    "retries": 3
}

with DAG(
    dag_id="s3_json_file_to_snowflake_wh",
    default_args=default_args, 
    description="Downloads JSON data from S3 Bucket and uploads to Snowflake Warehouse", 
    schedule=timedelta(minutes=10),
    start_date=datetime(2024, 6, 1), 
    catchup=False,
    tags=["s3", "snowflake", "json", "downlad", "s3 to snowflake"]
) as dag: 

    
    task_download_json_from_s3 = PythonOperator(
        task_id="download_json_from_s3",
        python_callable=download_json_from_s3
    )

    task_upload_json_to_snowflake = PythonOperator(
        task_id="upload_json_to_snowflake",
        python_callable=upload_s3_json_data_to_snowflake
    )

    task_copy_from_stage_to_table = SQLExecuteQueryOperator(
        task_id="copy_from_stage_to_table",
        conn_id="snowflake_default",
        sql="""
            COPY INTO STOCK_QUOTES.COMMON.RAW_STOCK_QUOTE_KAFKA_EVENTS(src, file_name, snowflake_ingest_ts)
                FROM (
                    SELECT $1, METADATA$FILENAME, CURRENT_TIMESTAMP()
                    FROM @STOCK_QUOTES.COMMON.RAW_STOCK_QUOTE_STAGING
                )
            FILE_FORMAT = (FORMAT_NAME = 'STOCK_QUOTES.COMMON.JSON_FILE_FORMAT')
            ON_ERROR = 'CONTINUE';
        """
    )

    # Dependancy
    task_download_json_from_s3 >> task_upload_json_to_snowflake >> task_copy_from_stage_to_table