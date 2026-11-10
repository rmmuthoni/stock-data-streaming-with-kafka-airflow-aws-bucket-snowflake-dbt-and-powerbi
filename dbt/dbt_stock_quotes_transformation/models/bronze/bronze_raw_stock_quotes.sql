SELECT 
    * 
FROM {{ source('source', 'raw_stock_quote_kafka_events') }}