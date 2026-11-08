import json 
import requests 
from confluent_kafka import Producer
import dotenv 

# load environment variables from .env file
dotenv.load_dotenv()

print(Producer)