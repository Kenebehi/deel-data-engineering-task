CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    order_date DATE,
    delivery_date DATE,
    customer_id BIGINT,
    status STRING,
    updated_at TIMESTAMP(3),
    updated_by BIGINT,
    created_at TIMESTAMP(3),
    created_by BIGINT
) WITH (
    'connector' = '{{ connector }}',
    'topic' = '{{ topic }}',
    'properties.bootstrap.servers' = '{{ bootstrap_servers }}',
    'properties.group.id' = '{{ consumer_group_id }}',
    'scan.startup.mode' = '{{ scan_startup_mode }}',
    'format' = '{{ format }}'
);