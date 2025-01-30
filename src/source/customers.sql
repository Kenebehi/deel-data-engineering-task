CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    customer_name STRING,
    is_active BOOLEAN,
    customer_address STRING,
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



