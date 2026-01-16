with orders as (
    select * from {{ ref('stg_orders') }}
),

payments as (
    select
        order_id,
        sum(amount) as total_amount
    from {{ ref('stg_payments') }}
    group by 1
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_status,
        o.purchased_at,
        p.total_amount
    from orders o
    left join payments p on o.order_id = p.order_id
)

select * from final