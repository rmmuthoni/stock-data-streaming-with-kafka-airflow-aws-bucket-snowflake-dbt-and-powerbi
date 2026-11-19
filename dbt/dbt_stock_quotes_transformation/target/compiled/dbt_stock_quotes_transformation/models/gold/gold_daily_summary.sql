
WITH gold_stock_quotes AS (
    SELECT 
        *
    FROM STOCK_QUOTES.dbt_rogers_gold.gold_stock_quotes
    
    WHERE market_day = (SELECT MAX(market_day) FROM STOCK_QUOTES.dbt_rogers_gold.gold_daily_summary)
    
),

latest_market_time AS (
    SELECT 
        MAX(fetched_at) AS fetched_at,
        market_day,
        symbol
    FROM gold_stock_quotes
    GROUP BY market_day, symbol
),

daily_summary AS (
    SELECT 
        l.fetched_at,
        current_price,
        l.symbol,
        l.market_day,
        prev_day_close,
        day_high,
        day_low,
        day_open,
        change_percent,
        change_amount,
        source_system,
        file_name,
        market_time,
        snowflake_ingest_ts
    FROM latest_market_time l
    LEFT JOIN gold_stock_quotes g
        ON l.fetched_at = g.fetched_at
)

SELECT * FROM daily_summary