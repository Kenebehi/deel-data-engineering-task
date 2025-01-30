CREATE TABLE top_delivery_dates_sink (
    delivery_date DATE PRIMARY KEY NOT ENFORCED,
    open_orders BIGINT,
    updated_at TIMESTAMP
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://0.0.0.0:5432/finance_db',
    'table-name' = 'open_orders_by_delivery',
    'username' = 'finance_db_user',
    'password' = '1234',
    'driver' = 'org.postgresql.Driver'
);
