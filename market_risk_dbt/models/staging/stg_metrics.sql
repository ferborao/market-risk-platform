with source as (
    select * from read_parquet('../data/silver/metrics.parquet')
),

staged as (
    select
        ticker,
        var_95,
        var_99,
        volatility,
        sharpe,
        max_drawdown
    from source
    order by ticker
)

select * from staged