with source as (
    select * from {{ source('raw_data', 'orders') }}
)

select
    order_id,
    customer_id,
    order_status,
    -- On convertit les strings en vrais types temporels
    cast(order_purchase_timestamp as timestamp) as purchased_at,
    cast(order_delivered_customer_date as timestamp) as delivered_at,
    cast(order_estimated_delivery_date as timestamp) as estimated_delivery_at
from source