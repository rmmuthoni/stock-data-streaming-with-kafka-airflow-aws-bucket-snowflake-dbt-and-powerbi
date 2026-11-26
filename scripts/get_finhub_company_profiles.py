import dotenv 
import os 
from typing import Any
import finnhub

# load environment variables from .env file
dotenv.load_dotenv()

API_KEY = os.getenv("FINHUB_API_KEY")
API_URL = os.getenv("FINHUB_API_COMPANY_PROFILE_URL")
SYMBOLS = ["AAPL", "NVDA", "MSFT", "AMZN", "SPCX", "GOOGL", "GOOG", "META", "AVGO", "TSLA", "AMD", "INTC", "NFLX", "ADBE", "CRM", "PYPL", "CSCO", "ORCL", "QCOM", "TXN"]

# Set up Finnhub Client
finnhub_client = finnhub.Client(api_key=API_KEY)


# Fetch Company Profile Data from Finnhub API 
def fetch_company_profile(symbol: str) -> Any:
    """Fetch company profile data from Finnhub API for a given stock symbol."""
    try:
        response = finnhub_client.company_profile2(symbol=symbol)
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return None
    else:
        if response:
            return response
        else:
            print(f"No data found for symbol: {symbol}")
            return None
