from typing import Optional
import uuid
from pydantic import Field
from src.models.domain.data_source.data_source_column import DataSourceColumn
from src.utils.base_schema import BaseSchema


class DataSourceColumnCreateSchema(BaseSchema):
    type: str = Field(description="Column type.")
    name: str = Field(description="Column name.")
    description: str = Field(description="Column brief description (used for context)")


class DataSourceColumnUpdateSchema(BaseSchema):
    type: Optional[str]
    name: Optional[str]
    description: Optional[str]


class DataSourceColumnSchema(DataSourceColumnCreateSchema):
    id: uuid.UUID = Field(description="Unique Indentifier", default_factory=uuid.uuid4)

    class Config(BaseSchema.Config):
        from_attributes = True
