import os

from sqlmesh.core.config import (
    BigQueryConnectionConfig,
    Config,
    DuckDBConnectionConfig,
    GatewayConfig,
    ModelDefaultsConfig,
)

CURRENT_FILE_PATH = os.path.abspath(__file__)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


defaults = {"dialect": "duckdb"}
model_defaults = ModelDefaultsConfig(**defaults)


config = Config(
    gateways={
        "bq": GatewayConfig(
            connection=BigQueryConnectionConfig(
                project=os.environ.get("GCP_PROJECT", None),
            ),
            state_connection=DuckDBConnectionConfig(database=f"{DATA_DIR}/bigquery.duckdb"),
        )
    },
    default_gateway="bq",
    model_defaults=model_defaults,
)
