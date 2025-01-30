CREATE TABLE pending_items_by_product_sink (
    product_id BIGINT PRIMARY KEY NOT ENFORCED,
    pending_items BIGINT,
    updated_at TIMESTAMP
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://0.0.0.0:5432/finance_db',
    'table-name' = 'open_orders_by_delivery',
    'username' = 'finance_db_user',
    'password' = '1234',
    'driver' = 'org.postgresql.Driver'
);
