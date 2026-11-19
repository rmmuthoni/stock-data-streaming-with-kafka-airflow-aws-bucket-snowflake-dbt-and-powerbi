
-- We are using append strategy since bronze is an as-is copy of the raw source
-- Therefore, the strategy will only append new records at the bottom of the table

SELECT 
    * 
FROM stock_quotes.common.raw_stock_quote_kafka_events

WHERE snowflake_ingest_ts > (SELECT MAX(snowflake_ingest_ts) FROM STOCK_QUOTES.dbt_rogers_bronze.bronze_raw_stock_quotes)
