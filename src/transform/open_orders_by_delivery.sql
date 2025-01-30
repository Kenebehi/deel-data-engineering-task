INSERT INTO open_orders_by_delivery_sink
SELECT 
    delivery_date, 
    status, 
    COUNT(order_id) AS open_orders,
    CURRENT_TIMESTAMP
FROM orders
WHERE status IN ('OPEN', 'PENDING')
GROUP BY delivery_date, status;
