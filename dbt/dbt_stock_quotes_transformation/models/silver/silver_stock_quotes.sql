{{
  config(
    materialized = 'incremental',
    unique_key = 'file_name',
    incremental_strategy = 'merge',
    on_schema_change = 'sync_all_columns'
    )
}}
-- Merge strategy so that records are updated rather than treated as new records 
-- Using file name (which is immutable) to track unique records
WITH raw_stock_quotes_json AS (
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY file_name ORDER BY snowflake_ingest_ts DESC) AS record_rank
    FROM {{ ref('bronze_raw_stock_quotes') }}
    {% if is_incremental() %}
    WHERE snowflake_ingest_ts > (SELECT MAX(snowflake_ingest_ts) FROM {{ this }} AS t)
    {% endif %}
), 

-- Remove possible duplicate records commong with Kafka Stream Rebalancing
deduplicate_raw_stock_quotes_json AS (
    SELECT 
        *
    FROM raw_stock_quotes_json 
    WHERE record_rank = 1
),

-- Extract and structure the raw stock quotes from JSON to a more structured format
structured_raw_stock_quotes AS (
    SELECT 
        src:c::FLOAT AS current_price,
        src:d::FLOAT AS change_amount,
        src:dp::FLOAT AS change_percent,
        src:h::FLOAT AS day_high,
        src:l::FLOAT AS day_low,
        src:o::FLOAT AS day_open,
        src:pc::FLOAT AS prev_day_close,
        src:symbol::STRING AS symbol,
        TO_TIMESTAMP_NTZ(src:t::NUMBER) AS market_time,
        src:fetched_at::TIMESTAMP_NTZ AS fetched_at,
        src:source_system::STRING AS source_system,
        file_name,
        snowflake_ingest_ts
    FROM deduplicate_raw_stock_quotes_json
),

-- Clean Floating Point Values to 2 Decimal Places
cleaned_stock_quotes AS (
    SELECT
        ROUND(current_price, 2) AS current_price,
        ROUND(change_amount, 2) AS change_amount,
        ROUND(change_percent, 2) AS change_percent,
        ROUND(day_high, 2) AS day_high,
        ROUND(day_low, 2) AS day_low,
        ROUND(day_open, 2) AS day_open,
        ROUND(prev_day_close, 2) AS prev_day_close,
        TRIM(symbol) as symbol,
        market_time,
        TO_DATE(market_time) AS market_day,
        fetched_at,
        TRIM(source_system) AS source_system,
        file_name,
        snowflake_ingest_ts
    FROM structured_raw_stock_quotes
),

finally AS (
    SELECT * FROM cleaned_stock_quotes
)

SELECT * FROM finally