with source as (
    select * from read_parquet('../data/silver/correlations.parquet')
),

staged as (
    select *        
    from source        
)

select * from staged