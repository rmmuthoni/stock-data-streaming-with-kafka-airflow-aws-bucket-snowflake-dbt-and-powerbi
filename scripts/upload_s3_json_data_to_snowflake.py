from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook 
import snowflake.connector as snowflake_connector 

from pathlib import Path

from dotenv import load_dotenv 

# Loand Environ;ment Variables 
load_dotenv()

def upload_s3_json_data_to_snowflake(**context) -> None: 
    """Pulls a list of local file paths from XCom and uploads to Snowflake STAGE"""

    # Pull the files from XCom
    local_file_paths = context["ti"].xcom_pull(task_ids="download_json_from_s3", key="downloaded_s3_files")
    if not local_file_paths:
        print("No files paths found in XCom. Skipping snowflake Upload")

    # Connect to Snowflake Warehouse
    snowflake_hook = SnowflakeHook(snowflake_conn_id="snowflake_default")
    with snowflake_hook.get_conn() as conn:
        with conn.cursor() as cursor:

            for local_file_path in local_file_paths:
                local_file_path = Path(local_file_path) 
                if not local_file_path.exists():
                    print(f"{str(local_file_path)} does not exists: Proceeding")
                    continue
                # Put the Json File into the Snowflake STAGE
                put_sql = f"PUT file://{str(local_file_path)} @STOCK_QUOTES.COMMON.RAW_STOCK_QUOTE_STAGING AUTO_COMPRESS=TRUE;"
                cursor.execute(put_sql) 

    # After successfull upload, we clean the folder 
    print(f"Performing Clean-up of local Airflow Storage")
    for local_file_path in local_file_paths:
        local_file_path = Path(local_file_path)
        local_file_path.unlink(missing_ok=True)


