{{
  config(
    materialized = 'incremental',
    unique_key = 'record_id',
    incremental_strategy = 'merge',
    on_schema_change = 'append_new_columns'
    )
}}

WITH silver_stock_quotes AS (
    SELECT 
        *
    FROM {{ ref('silver_stock_data') }}
    {% if is_incremental() %}
    WHERE record_id > (SELECT MAX(record_id) FROM {{ this }})
    {% endif %}
)

SELECT * FROM silver_stock_quotes