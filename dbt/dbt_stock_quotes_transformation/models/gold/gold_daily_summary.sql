{{
  config(
    materialized = 'incremental',
    unique_key = 'symbol',
    incremental_strategy = 'merge',
    on_schema_change = 'sync_all_columns'
    )
}}
WITH gold_stock_quotes AS (
    SELECT 
        *
    FROM {{ ref('gold_stock_data') }}
    {% if is_incremental() %}
    WHERE market_day >= (SELECT MAX(market_day) FROM {{ this }})
    {% endif %}
),

latest_market_time AS (
    SELECT 
        MAX(record_id) AS record_id,
        --market_day,
        symbol
    FROM gold_stock_quotes
    GROUP BY symbol
),

daily_summary AS (
    SELECT 
        --l.fetched_at,
        g.record_id,
        g.market_day,
        l.symbol,
        current_price,
        
        prev_day_close,
        day_high,
        day_low,
        day_open,
        change_amount,
        change_percent,
        
        --source_system,
        --file_name,
        market_time,
        --snowflake_ingest_ts
    FROM latest_market_time l
    LEFT JOIN gold_stock_quotes g
        ON l.record_id = g.record_id
)

SELECT * FROM daily_summary
