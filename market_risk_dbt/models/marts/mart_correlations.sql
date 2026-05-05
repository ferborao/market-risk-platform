
with source as (
    select * from {{ ref('stg_correlations') }}
),

unpivoted as (
    UNPIVOT source
    ON COLUMNS(* EXCLUDE ticker)
    INTO
        NAME ticker_b
        VALUE correlation
)

select
    ticker as ticker_a,
    ticker_b,
    round(correlation, 4) as correlation
from unpivoted
order by ticker_a, ticker_b