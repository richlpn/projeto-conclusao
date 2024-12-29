from typing import Optional
import uuid
from pydantic import Field
from src.models.domain.data_source.data_source_column import DataSourceColumn
from src.schema.base_schema import BaseSchema


class DataSourceColumnCreateSchema(BaseSchema):
    type: str = Field(description="Column type.")
    name: str = Field(description="Column name.")
    description: str = Field(description="Column brief description (used for context)")
    data_source_id: uuid.UUID = Field()


class DataSourceColumnUpdateSchema(BaseSchema):
    type: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class DataSourceColumnSchema(DataSourceColumnCreateSchema):
    id: uuid.UUID = Field(description="Unique Indentifier", default_factory=uuid.uuid4)
    data_source_id: uuid.UUID = Field()

    class Config(BaseSchema.Config):
        from_attributes = True
