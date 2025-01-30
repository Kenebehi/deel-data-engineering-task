INSERT INTO pending_items_by_product_sink
SELECT 
    oi.product_id, 
    SUM(oi.quantity) AS pending_items, 
    CURRENT_TIMESTAMP
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'PENDING'
GROUP BY oi.product_id;
