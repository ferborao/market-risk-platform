
with source as (
    select * from {{ ref('stg_metrics') }}
),

risk_metrics as (
    select *,
        case
            when volatility > 0.3 then 'High'
            when volatility > 0.2 then 'Medium'
            else 'Low'
        end as risk_level        
    from source
)

select * from risk_metrics