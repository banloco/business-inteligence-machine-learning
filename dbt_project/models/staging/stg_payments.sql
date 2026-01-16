with source as (
    select * from {{ source('raw_data', 'order_payments') }}
)

select
    order_id,
    payment_type,
    payment_installments,
    payment_value as amount
from source