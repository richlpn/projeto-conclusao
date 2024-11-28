import uuid

from pydantic import Field
from src.models.domain.data_source.data_source import DataSource, DataSourceType
from src.schema.data_source_column_schema import DataSourceColumnCreateSchema
from src.utils.base_schema import BaseSchema


class DataSourceCreateSchema(BaseSchema[DataSource]):
    name: str = Field(description="Data Source Name")
    type: DataSourceType = Field(description="Type of the data source.")
    columns: list[DataSourceColumnCreateSchema] = Field(
        default_factory=list, description="Columns used or referenced on the table."
    )
    separator: str | None = Field(
        default=None,
        description="Separator used only to describe the sperator of a CSV. If not informed must be set to None",
    )


class DataSourceUpdateSchema(BaseSchema[DataSource]):
    name: str
    type: DataSourceType
    separator: str | None


class DataSourceSchema:
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config(BaseSchema.Config):
        from_attributes = True
