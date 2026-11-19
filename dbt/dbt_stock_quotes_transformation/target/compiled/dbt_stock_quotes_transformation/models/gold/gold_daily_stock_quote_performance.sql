WITH gold_stock_quotes AS (
    SELECT 
        *
    FROM STOCK_QUOTES.dbt_rogers_gold.gold_stock_quotes
),

daily_stock_quote_aggregate AS (
    SELECT 
        symbol,
        market_day,
        ROUND(AVG(current_price), 2) AS avg_current_price
    FROM gold_stock_quotes 
    GROUP BY symbol, market_day
    HAVING symbol = 'CSCO'
)

SELECT * FROM gold_stock_quotes