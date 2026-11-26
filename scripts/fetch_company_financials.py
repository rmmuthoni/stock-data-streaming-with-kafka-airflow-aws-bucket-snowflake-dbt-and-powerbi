import dotenv 
import os 
from typing import Any
import finnhub
from pathlib import Path
from datetime import datetime
import time
import json

# load environment variables from .env file
dotenv.load_dotenv()

API_KEY = os.getenv("FINHUB_API_KEY")
API_URL = os.getenv("FINHUB_API_COMPANY_PROFILE_URL")
SYMBOLS = ["AAPL", "NVDA", "MSFT", "AMZN", "SPCX", "GOOGL", "GOOG", "META", "AVGO", "TSLA", "AMD", "INTC", "NFLX", "ADBE", "CRM", "PYPL", "CSCO", "ORCL", "QCOM", "TXN"]


 # Storage Folder - Create if Not Exists
BASE_DIR = Path(os.getenv('AIRFLOW_HOME', Path(__file__).resolve().parent.parent))
DATA_DIR = BASE_DIR / "data/financials/"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Set up Finnhub Client
finnhub_client = finnhub.Client(api_key=API_KEY)


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

def save_financials_to_file() -> None:
    """Save the fetched financials to a JSON file."""

    # Store filepaths and pass to XCOM
    file_paths = []

    # Loop through the symbols and fetch financials
    for symbol in SYMBOLS:
        financials = fetch_company_financials(symbol)
        # Add a timestamp to the filename to avoid overwriting files and to keep track of when the data was fetched
        financials["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save the financials to a JSON file in the data/financials/ directory
        if financials:
            # Create the directory if it doesn't exist
            file_path = DATA_DIR / f"{symbol}_financials_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)  
            
            with open(file_path, "w") as f:
                json.dump(financials, f)

            file_paths.append(str(file_path))

            print(f"Saved financials for {symbol} to {file_path}")
            
            # Sleep for 1 second to avoid hitting API rate limits
            time.sleep(1)

        else:
            print(f"Failed to fetch financials for {symbol}")

save_financials_to_file()