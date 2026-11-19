begin;
    insert into STOCK_QUOTES.dbt_rogers_bronze.bronze_raw_stock_quotes ("SRC", "FILE_NAME", "SNOWFLAKE_INGEST_TS")
    (
        select "SRC", "FILE_NAME", "SNOWFLAKE_INGEST_TS"
        from STOCK_QUOTES.dbt_rogers_bronze.bronze_raw_stock_quotes__dbt_tmp
    )

;
    commit;