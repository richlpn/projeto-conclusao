import uuid

from pydantic import Field
from src.schema.base_schema import BaseSchema


class Script(BaseSchema):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    code: str = Field(..., description="The python script code")

    class Config(BaseSchema.Config):
        from_attributes = True
