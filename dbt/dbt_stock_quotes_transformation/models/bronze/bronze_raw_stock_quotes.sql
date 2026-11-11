{{
  config(
    materialized = 'incremental',
    incremental_strategy = 'append',
    on_schema_change = 'append_new_columns'
    )
}}
-- We are using append strategy since bronze is an as-is copy of the raw source
-- Therefore, the strategy will only append new records at the bottom of the table

SELECT 
    * 
FROM {{ source('source', 'raw_stock_quote_kafka_events') }}
{% if is_incremental() %}
WHERE snowflake_ingest_ts > (SELECT MAX(snowflake_ingest_ts) FROM {{ this }})
{% endif %}