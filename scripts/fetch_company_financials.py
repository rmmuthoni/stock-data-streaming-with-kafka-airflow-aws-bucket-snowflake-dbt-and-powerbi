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
