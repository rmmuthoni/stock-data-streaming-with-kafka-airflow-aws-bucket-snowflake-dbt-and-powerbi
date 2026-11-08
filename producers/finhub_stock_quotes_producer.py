import json 
import requests 
from confluent_kafka import Producer
import dotenv 
import os 
from datetime import datetime
import time 
from typing import Any

# load environment variables from .env file
dotenv.load_dotenv()

API_KEY = os.getenv("FINHUB_API_KEY")
API_URL = os.getenv("FINHUB_API_URL")
SYMBOLS = ["AAPL"]

producer_config = {
    "bootstrap.servers": "host.docker.internal:9092",
    "client.id": "finhub-stock-data-producer"
}

producer = Producer(
    producer_config
)

def delivery_report(error, message) -> Any: 
    """Sends back a report if the producer topic was created"""
    if error:
        print("Error, Delivery Failed", error)
    print("Delivery Successful", message.value().decode("utf-8"))


# Fetch Stock Data from Finnhub API 
def fetch_stock_data(symbol: str) -> Any:
    """Fetch stock data for a given symbol from Finnhub API."""
    TARGET_URL = f"{API_URL}?symbol={symbol}&token={API_KEY}"

    try:
        response = requests.get(TARGET_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    else:
        # In case no errors were thrown, process the response 
        data = response.json()

        # Attach symbol and time metadata
        data["symbol"] = symbol 
        data["fetched_at"] = datetime.now().isoformat()

        print(data)
        return data

# Stream 
while True:
    for symbol in SYMBOLS:
        stock_quote = fetch_stock_data(symbol=symbol)
        if stock_quote:
            producer.produce("stock-quotes", value=json.dumps(stock_quote).encode("utf-8"), callback=delivery_report)
            producer.flush()
            time.sleep(4)
