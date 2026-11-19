

WITH silver_stock_quotes AS (
    SELECT 
        *
    FROM STOCK_QUOTES.dbt_rogers_silver.silver_stock_quotes
    
    WHERE snowflake_ingest_ts > (SELECT MAX(snowflake_ingest_ts) FROM STOCK_QUOTES.dbt_rogers_gold.gold_stock_quotes)
    
)

SELECT * FROM silver_stock_quotes