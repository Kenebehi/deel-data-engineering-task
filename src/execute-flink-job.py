import os
from dataclasses import asdict, dataclass, field
from typing import List, Tuple

from jinja2 import Environment, FileSystemLoader
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

# dependency jars to read data from kafka, and connect to postgres
REQUIRED_JARS = [
    "file:///opt/flink/flink-sql-connector-kafka-1.17.0.jar",
    "file:///opt/flink/flink-connector-jdbc-3.0.0-1.16.jar",
    "file:///opt/flink/postgresql-42.6.0.jar",
]


@dataclass(frozen=True)
class StreamJobConfig:
    job_name: str = 'execute-flink-job'
    jars: List[str] = field(default_factory=lambda: REQUIRED_JARS)
    checkpoint_interval: int = 10
    checkpoint_pause: int = 5
    checkpoint_timeout: int = 5
    parallelism: int = 2


@dataclass(frozen=True)
class KafkaConfig:
    connector: str = 'kafka'
    bootstrap_servers: str = 'kafka:9092'
    scan_startup_mode: str = 'earliest-offset'
    consumer_group_id: str = 'flink-consumer-group-1'
    format: str = 'json'


@dataclass(frozen=True)
class ProductsTopicConfig(KafkaConfig):
    topic: str = 'debezium.operations.products'


@dataclass(frozen=True)
class OrdersTopicConfig(KafkaConfig):
    topic: str = 'debezium.operations.orders'


@dataclass(frozen=True)
class OrderItemsTopicConfig(KafkaConfig):
    topic: str = 'debezium.operations.order_items'


@dataclass(frozen=True)
class CustomersTopicConfig(KafkaConfig):
    topic: str = 'debezium.operations.customers'


@dataclass(frozen=True)
class ApplicationDatabaseConfig:
    connector: str = 'jdbc'
    url: str = 'jdbc:postgresql://0.0.0.0:5432/finance_db'
    username: str = os.getenv("DB_USERNAME", "finance_db_user")
    password: str = os.getenv("DB_PASSWORD", "1234")
    driver: str = 'org.postgresql.Driver'


def get_execution_environment(
    config: StreamJobConfig,
) -> Tuple[StreamExecutionEnvironment, StreamTableEnvironment]:
    s_env = StreamExecutionEnvironment.get_execution_environment()
    for jar in config.jars:
        s_env.add_jars(jar)
    # start a checkpoint every 10,000 ms (10 s)
    s_env.enable_checkpointing(config.checkpoint_interval * 1000)
    # make sure 5000 ms (5 s) of progress happen between checkpoints
    s_env.get_checkpoint_config().set_min_pause_between_checkpoints(
        config.checkpoint_pause * 1000
    )
    # checkpoints have to complete within 5 minute, or are discarded
    s_env.get_checkpoint_config().set_checkpoint_timeout(
        config.checkpoint_timeout * 1000
    )
    execution_config = s_env.get_config()
    execution_config.set_parallelism(config.parallelism)
    t_env = StreamTableEnvironment.create(s_env)
    job_config = t_env.get_config().get_configuration()
    job_config.set_string("pipeline.name", config.job_name)
    return s_env, t_env


def get_sql_query(
    entity: str,
    type: str = 'source',
    template_env: Environment = Environment(loader=FileSystemLoader("src/")),
) -> str:
    config_map = {
        'orders': OrdersTopicConfig(),
        'order_items': OrderItemsTopicConfig(),
        'customers': CustomersTopicConfig(),
        'products': ProductsTopicConfig(),
    }

    return template_env.get_template(f"{type}/{entity}.sql").render(
        asdict(config_map.get(entity))
    )


def run_flink_job(
    t_env: StreamTableEnvironment,
    get_sql_query=get_sql_query,
) -> None:
    
    try:
        # Create Source DDLs
        t_env.execute_sql(get_sql_query('orders'))
        t_env.execute_sql(get_sql_query('order_items'))
        t_env.execute_sql(get_sql_query('customers'))
        t_env.execute_sql(get_sql_query('products'))

        # Create Sink DDL
        t_env.execute_sql(get_sql_query('open_orders_by_delivery', 'sink'))
        t_env.execute_sql(get_sql_query('top_delivery_dates', 'sink'))
        t_env.execute_sql(get_sql_query('pending_items_by_product', 'sink'))
        t_env.execute_sql(get_sql_query('top_customers_pending_orders', 'sink'))

        # Run transformation query
        stmt_set = t_env.create_statement_set()
        stmt_set.add_insert_sql(get_sql_query('open_orders_by_delivery', 'process'))
        stmt_set.add_insert_sql(get_sql_query('top_delivery_dates', 'process'))
        stmt_set.add_insert_sql(get_sql_query('pending_items_by_product', 'process'))
        stmt_set.add_insert_sql(get_sql_query('top_customers_pending_orders', 'process'))
    except Exception as e:
        print(f"Failed to execute SQL: {e}")


    execute_flink_job = stmt_set.execute()
    print(
        f"""
        Async sink job
         status: {execute_flink_job.get_job_client().get_job_status()}
        """
    )


if __name__ == '__main__':
    _, t_env = get_execution_environment(StreamJobConfig())
    run_flink_job(t_env)
