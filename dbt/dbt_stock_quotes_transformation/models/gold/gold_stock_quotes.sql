WITH silver_stock_quotes AS (
    SELECT 
        *
    FROM {{ ref('silver_stock_quotes') }}
)

SELECT * FROM silver_stock_quotes