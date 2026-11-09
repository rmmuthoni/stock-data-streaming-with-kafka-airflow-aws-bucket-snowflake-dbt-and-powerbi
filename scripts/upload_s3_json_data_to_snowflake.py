from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook 
import snowflake.connector as snowflake_connector 

from dotenv import load_dotenv 

# Loand Environ;ment Variables 
load_dotenv()

def upload_s3_json_data_to_snowflake(**context) -> None: 
    """Pulls a list of local file paths from XCom and uploads to Snowflake STAGE"""

    # Pull the files from XCom
    local_file_paths = context["ti"].xxom_pull(task_ids="download_json_from_s3")
    if not local_file_paths:
        print("No files paths found in XCom. Skipping snowflake Upload")

    # Connect to Snowflake Warehouse

