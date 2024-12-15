import uuid
from typing import Optional

from pydantic import Field
from src.schema.base_schema import BaseSchema
from src.schema.data_source_column_schema import DataSourceColumnSchema
from src.schema.data_source_type_schema import DataSourceTypeSchema


class DataSourceCreateSchema(BaseSchema):
    name: str = Field(description="Data Source Name")
    type: uuid.UUID = Field(description="Id of the type of the data source.")

    separator: str | None = Field(
        default=None,
        description="Separator used only to describe the sperator of a CSV. If not informed must be set to None",
    )


class DataSourceUpdateSchema(BaseSchema):
    name: Optional[str] = Field(default=None)
    type: Optional[uuid.UUID] = Field(default=None)
    separator: Optional[str] = Field(default=None)


class DataSourceSchema(DataSourceCreateSchema):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    type: DataSourceTypeSchema = Field(description="File type.")  # type: ignore
    columns: list[DataSourceColumnSchema] = Field(  # type: ignore
        default_factory=list, description="Columns used or referenced on the table."
    )

    class Config(BaseSchema.Config):
        from_attributes = True
