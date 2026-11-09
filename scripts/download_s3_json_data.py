import boto3 
from dotenv import load_dotenv 
import os 
from pathlib import Path 

# Load Environment Variables
load_dotenv() 

def download_json_from_s3() -> list:
    """Download JSON files from S3 bucket to local directory."""

    # Storage Folder - Create if Not Exists
    BASE_DIR = Path(os.getenv('AIRFLOW_HOME', Path(__file__).resolve().parent.parent))
    DATA_DIR = BASE_DIR / "data/stock_quotes/"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Store the downloaded files in this list
    DOWNLOADED_FILES = [] 

    # S3 Bucket set up
    s3_client = boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    bucket_name = os.getenv("S3_STOCKS_BUCKET_NAME")

    # Fetch objects in the bucket
    stored_objects = s3_client.list_objects(Bucket=os.getenv("S3_STOCKS_BUCKET_NAME")).get("Contents", [])

    for object in stored_objects:
        key = object["Key"]
        local_json_file_name = DATA_DIR / os.path.basename(key)

        # Download the files and Append to the List
        s3_client.download_file(bucket_name, key, local_json_file_name)
        print(f"S3 Json File Downloaded: {local_json_file_name}")

        DOWNLOADED_FILES.append(str(local_json_file_name)) 
        print(local_json_file_name)  

    return DOWNLOADED_FILES