INSERT INTO top_delivery_dates_sink
SELECT 
    delivery_date, 
    open_orders, 
    CURRENT_TIMESTAMP
FROM (
    SELECT 
        delivery_date, 
        COUNT(order_id) AS open_orders,
        ROW_NUMBER() OVER (ORDER BY COUNT(order_id) DESC) AS rank
    FROM orders
    WHERE status = 'OPEN'
    GROUP BY delivery_date
) ranked_orders
WHERE rank <= 3;
