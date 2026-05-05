with source as (
    select * from read_parquet('../data/silver/returns.parquet')
),

staged as (
    select
        Date,
        ticker,
        Close,
        log_return
    from source
    order by ticker, Date
)

select * from staged