CREATE TABLE open_orders_by_delivery_sink (
    delivery_date DATE,
    status STRING,
    open_orders BIGINT,
    updated_at TIMESTAMP,
    PRIMARY KEY (delivery_date, status) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://0.0.0.0:5432/finance_db',
    'table-name' = 'open_orders_by_delivery',
    'username' = 'finance_db_user',
    'password' = '1234',
    'driver' = 'org.postgresql.Driver'
);
