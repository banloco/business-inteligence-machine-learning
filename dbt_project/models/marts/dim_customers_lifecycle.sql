with orders as (
    select * from {{ ref('fct_orders') }}
),

customer_metrics as (
    select
        customer_id,
        min(purchased_at) as first_purchase_at,
        count(order_id) as total_orders,
        sum(total_amount) as lifetime_value
    from orders
    group by 1
)

select * from customer_metrics