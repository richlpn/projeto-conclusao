""""""
from pydantic import BaseModel, Field


class ColumnSchema(BaseModel):
    type: str = Field(default="str", description="Column type.")
    name: str = Field(default="str", description="Column name.")
    description: str = Field(description="Column brief description (used for context)")


class TableSchema(BaseModel):
    name: str = Field(description="Table Name")
    columns: list[ColumnSchema] = Field(
        default_factory=list, description="Columns used or referenced on the table."
    )


class DataSourceSchema(BaseModel):
    name: str = Field(description="Data Source Name")
    tables: list[TableSchema] = Field(
        default_factory=list, description="Tables referenced on the data."
    )