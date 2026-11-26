import dotenv 
import os 
from typing import Any
from pathlib import Path
from datetime import datetime
import time
import json
import finnhub
import settings

# Set up Finnhub Client
finnhub_client = finnhub.Client(api_key=settings.API_KEY)


# Setup S3 Client 
s3_client = settings.AWS_S3_COMMON_CLIENT
bucket_name = os.getenv("S3_FINANCIALS_BUCKET_NAME")


# Fetch Company financials from finhup API
def fetch_company_financials(symbol: str) -> dict[str, Any] | None:
    """Fetch company financials from Finnhub API for a given stock symbol."""    
    try:
        response = finnhub_client.company_basic_financials(symbol=symbol, metric='all')
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return None
    else:
        if response:
            return response.get("metric", {})
        else:
            print(f"No data found for symbol: {symbol}")
            return None


def save_financials_to_s3() -> None:
    """Save the fetched financials to a JSON file."""
    for symbol in settings.SYMBOLS:
        company_financials = fetch_company_financials(symbol)

        if company_financials:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            company_financials["timestamp"] = timestamp

            s3_file_key = f"new/{symbol}-financials-{timestamp}.json"

            try:
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_file_key,
                    Body=json.dumps(company_financials),
                    ContentType="application/json"
                )
                print(f"Success: {symbol} financials put into S3 Bucket. Buckent = {bucket_name}")
            except Exception as e:
                print(f"Error Uploading {symbol} financials to S3: Error = {e}")
        
        time.sleep(1)


save_financials_to_s3()