CREATE TABLE top_customers_pending_orders_sink (
    customer_id BIGINT PRIMARY KEY NOT ENFORCED,
    customer_name STRING,
    pending_orders BIGINT,
    updated_at TIMESTAMP
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://0.0.0.0:5432/finance_db',
    'table-name' = 'open_orders_by_delivery',
    'username' = 'finance_db_user',
    'password' = '1234',
    'driver' = 'org.postgresql.Driver'
);
