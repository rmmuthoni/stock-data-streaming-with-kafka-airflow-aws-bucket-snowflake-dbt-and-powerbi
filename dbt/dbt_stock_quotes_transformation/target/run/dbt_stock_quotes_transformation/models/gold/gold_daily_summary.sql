begin;
    
        
        
        delete from DEV_STOCK_MARKET.dbt_rogers_gold.gold_daily_summary as DBT_INTERNAL_DEST
        where (record_id) in (
            select distinct record_id
            from DEV_STOCK_MARKET.dbt_rogers_gold.gold_daily_summary__dbt_tmp as DBT_INTERNAL_SOURCE
        );

    

    insert into DEV_STOCK_MARKET.dbt_rogers_gold.gold_daily_summary ("RECORD_ID", "MARKET_DAY", "SYMBOL", "CURRENT_PRICE", "PREV_DAY_CLOSE", "DAY_HIGH", "DAY_LOW", "DAY_OPEN", "CHANGE_AMOUNT", "CHANGE_PERCENT", "MARKET_TIME")
    (
        select "RECORD_ID", "MARKET_DAY", "SYMBOL", "CURRENT_PRICE", "PREV_DAY_CLOSE", "DAY_HIGH", "DAY_LOW", "DAY_OPEN", "CHANGE_AMOUNT", "CHANGE_PERCENT", "MARKET_TIME"
        from DEV_STOCK_MARKET.dbt_rogers_gold.gold_daily_summary__dbt_tmp
    );
    commit;