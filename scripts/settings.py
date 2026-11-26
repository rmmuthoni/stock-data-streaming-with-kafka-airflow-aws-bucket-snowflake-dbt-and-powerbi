from pathlib import Path
import os
import boto3 
from dotenv import load_dotenv 


# LOAD ENVIRONMENT VARIABLES 
load_dotenv()

# DEFINE THE API KEY AND URL FOR FINNHUB
API_KEY = os.getenv("FINHUB_API_KEY")
API_URL = os.getenv("FINHUB_API_COMPANY_PROFILE_URL")

# DEFINE THE STOCK SYMBOLS TO FETCH FINANCIALS FOR 
SYMBOLS = ["AAPL", "NVDA", "MSFT", "AMZN", "SPCX", "GOOGL", "GOOG", "META", "AVGO", "TSLA", "AMD", "INTC", "NFLX", "ADBE", "CRM", "PYPL", "CSCO", "ORCL", "QCOM", "TXN"]


# DEFINE THE BASE DIRECTORY FOR THE PROJECT
BASE_DIR = Path(os.getenv('AIRFLOW_HOME', Path(__file__).resolve().parent.parent))

# Storage Folder Location for Financials 
FINANCIAL_DATA_DIR = BASE_DIR / "data/financials/"
FINANCIAL_DATA_DIR.mkdir(parents=True, exist_ok=True)

# AWS S3 CLIENT COMMON SETTINGS 
AWS_S3_COMMON_CLIENT = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

S3_STOCKS_BUCKET_NAME = os.getenv("S3_STOCKS_BUCKET_NAME")
S3_FINANCIALS_BUCKET_NAME = os.getenv("S3_FINANCIALS_BUCKET_NAME")

