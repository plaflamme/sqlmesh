from __future__ import annotations

import logging
import typing as t

from sqlglot import exp

from sqlmesh.core.engine_adapter.base_postgres import BasePostgresEngineAdapter
from sqlmesh.core.engine_adapter.mixins import (
    GetCurrentCatalogFromFunctionMixin,
    PandasNativeFetchDFSupportMixin,
)
from sqlmesh.core.engine_adapter.shared import set_catalog
from sqlmesh.utils.errors import SQLMeshError

if t.TYPE_CHECKING:
    from sqlmesh.core._typing import SchemaName, TableName

logger = logging.getLogger(__name__)


@set_catalog()
class CloudSpannerEngineAdapter(
    BasePostgresEngineAdapter,
    PandasNativeFetchDFSupportMixin,
    GetCurrentCatalogFromFunctionMixin,
):
    DIALECT = "postgres"
    SUPPORTS_INDEXES = True
    HAS_VIEW_BINDING = True
    CURRENT_CATALOG_EXPRESSION = exp.column("current_catalog")
    SUPPORTS_REPLACE_TABLE = False

    def columns(
        self, table_name: TableName, include_pseudo_columns: bool = False
    ) -> t.Dict[str, exp.DataType]:
        table = exp.to_table(table_name)
        resp = self.cursor.get_table_column_schema(table.alias_or_name)
        return {
            column_name: exp.DataType.build(data_type, dialect=self.dialect, udt=True)
            for column_name, data_type in resp
        }

    def table_exists(self, table_name: TableName) -> bool:
        table = exp.to_table(table_name)
        table.db
        tables = self.cursor.list_tables()
        return table in tables

    def create_schema(
        self, schema_name: SchemaName, ignore_if_exists: bool = True, warn_on_error: bool = True
    ) -> None:
        # IF NOT EXISTS is not supported for CREATE SCHEMA
        #   Assume the schema exists
        # TODO: check if the schema exists
        return None

    def create_state_table(
        self,
        table_name: str,
        columns_to_types: t.Dict[str, exp.DataType],
        primary_key: t.Optional[t.Tuple[str, ...]] = None,
    ) -> None:
        if primary_key is None:
            raise SQLMeshError(
                f"Invalid table schema '{table_name}': Cloud Spanner requires a primary key on all tables"
            )
        table = exp.to_table(table_name)
        if table.alias_or_name.startswith("_"):
            raise SQLMeshError(
                f"Invalid table name '{table_name}': Cloud Spanner table names mmust start with a letter"
            )

        return super().create_state_table(table_name, columns_to_types, primary_key)
