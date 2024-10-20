""""""

from pydantic import BaseModel, Field


class ColumnSchema(BaseModel):
    type: str = Field(default="str", description="Column type.")
    name: str = Field(default="str", description="Column name.")
    description: str = Field(description="Column brief description (used for context)")


class TableSchema(BaseModel):

    type: str = Field(
        description="Any type of structured or semi-structure data source (CSV, SQL, XLSX, JSON, etc...)"
    )
    name: str = Field(
        description="Name of the table used for extraction and database connections."
    )
    columns: list[ColumnSchema] = Field(
        default_factory=list, description="Columns used or referenced on the table."
    )


class DataSourceSchema(BaseModel):
    name: str = Field(description="Data Source Name")
    tables: list[TableSchema] = Field(
        default_factory=list, description="Tables referenced on the data."
    )
