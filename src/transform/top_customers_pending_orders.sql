INSERT INTO top_customers_pending_orders_sink
SELECT 
    o.customer_id, 
    c.customer_name, 
    COUNT(o.order_id) AS pending_orders,
    CURRENT_TIMESTAMP
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'PENDING'
GROUP BY o.customer_id, c.customer_name
ORDER BY pending_orders DESC
LIMIT 3;
