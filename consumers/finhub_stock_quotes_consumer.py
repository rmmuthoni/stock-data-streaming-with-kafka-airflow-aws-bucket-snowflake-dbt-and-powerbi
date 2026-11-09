from confluent_kafka import Consumer 
import json 
import boto3
import dotenv 
import os

# Load Environment Variables
dotenv.load_dotenv()

# Set Up the S3 Bucket 
s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
bucket_name = os.getenv("S3_STOCKS_BUCKET_NAME")


# Set up the Consumer
consumer_config = {
   "bootstrap.servers": "localhost:29092",
   "group.id": "stock_quote_consumer",
   "auto.offset.reset": "earliest"
}
consumer = Consumer(consumer_config)
consumer.subscribe(["stock-quotes"])

print("Consumer is running and subscribed to topic: stock-quotes")

# Consume new topics topics
while True:
    message = consumer.poll(timeout=1.0)
    if message is None:
        continue 
    if message.error():
        print("Ecountered an Error", message.error())
        continue 

    # If no errors, read the message stream 
    message_value = message.value().decode("utf-8")
    stock_quote = json.loads(message_value)
    timestamp = stock_quote.get("fetched_at")
    key = f"{stock_quote.get("symbol")}/{timestamp}.json"

    # Send the Quote to the buecket 
    try: 
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(stock_quote),
            ContentType="application/json"
        )
        print(f"Stock Quote {key} has been put in the Bucket: {bucket_name}")
    except Exception as e:
        print("Error Occured While Putting into S3 Bucket", e)