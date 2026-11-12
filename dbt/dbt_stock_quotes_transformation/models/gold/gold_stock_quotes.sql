{{
  config(
    materialized = 'incremental',
    unique_key = 'file_name',
    incremental_strategy = 'merge',
    on_schema_change = 'append_new_columns'
    )
}}

WITH silver_stock_quotes AS (
    SELECT 
        *
    FROM {{ ref('silver_stock_quotes') }}
    {% if is_incremental() %}
    WHERE snowflake_ingest_ts > (SELECT MAX(snowflake_ingest_ts) FROM {{ this }})
    {% endif %}
)

SELECT * FROM silver_stock_quotes