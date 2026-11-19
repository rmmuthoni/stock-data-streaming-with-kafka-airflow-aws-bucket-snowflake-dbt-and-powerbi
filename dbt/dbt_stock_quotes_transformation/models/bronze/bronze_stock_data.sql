-- This is an incremental model
-- Process only newly stored from the source 

{{
  config(
    materialized = 'incremental',
    incremental_strategy = 'append',
    on_schema_change = 'append_new_columns'
    )
}}

SELECT 
    * 
FROM {{ source('source', 'raw_stock_market_data') }} 
{% if is_incremental() %}
WHERE record_id > (SELECT MAX(record_id) FROM {{ this }})
{% endif %}