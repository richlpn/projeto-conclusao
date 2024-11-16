"""
Module containing Pydantic models for data documentation schemas.

These models define the structure and validation rules for data documentation,
including data sources, tables, columns, and data transformation operations.

The models in this module are used to validate and parse data documentation
schemas, ensuring that they conform to a standard format and contain the
required information.

Classes:
    ColumnSchema: Represents a column in a table, including its type, name, and description.
    DataSourceType: An enumeration of supported data source types (e.g., CSV, SQL, XLSX, JSON).
    TableSchema: Represents a table in a data source, including its type, name, columns, and separator.
    DataSourceSchema: Represents a data source, including its name, tables, and data transformation operations.

See Also:
    src.models.operations: Module containing Pydantic models for data transformation operations.
"""

from enum import Enum
from pydantic import BaseModel, Field

from src.models.operations import Operation


class ColumnSchema(BaseModel):
    type: str = Field(default="str", description="Column type.")
    name: str = Field(default="str", description="Column name.")
    description: str = Field(description="Column brief description (used for context)")


class DataSourceType(str, Enum):
    CSV = "csv"
    SQL = "sql"
    XLSX = "xlsx"
    JSON = "json"


class TableSchema(BaseModel):

    type: DataSourceType = Field(
        description="Type of the data source.", examples=list(DataSourceType)
    )
    name: str = Field(
        description="Name of the table used for extraction and database connections."
    )
    columns: list[ColumnSchema] = Field(
        default_factory=list, description="Columns used or referenced on the table."
    )
    separator: str | None = Field(
        default=None,
        description="Separator used only to describe the sperator of a CSV. If not informed must be set to None",
    )


class DataSourceSchema(BaseModel):
    name: str = Field(description="Data Source Name")
    tables: list[TableSchema] = Field(
        default_factory=list, description="Tables referenced on the data."
    )
    operations: list[Operation] = Field(
        default_factory=list, description="Data transformation operations."
    )
