from uuid import UUID, uuid4
from pydantic import Field
from src.schema.base_schema import BaseSchema


class DataSourceTypeCreateSchema(BaseSchema):
    name: str = Field(description="Data Source Name", max_length=10)


class DataSourceTypeUpdateSchema(DataSourceTypeCreateSchema):
    pass


class DataSourceTypeSchema(DataSourceTypeCreateSchema):
    id: UUID = Field(default_factory=uuid4)

    class Config(BaseSchema.Config):
        from_attributes = True
