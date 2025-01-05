from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field
from src.schema.base_schema import BaseSchema


class TaskUpdateSchema(BaseSchema):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(
        default=None,
        max_length=400,
    )
    signature_function: Optional[str] = Field(default=None)


class TaskCreateSchema(BaseSchema):
    title: Optional[str] = Field(description="A short descriptive title about the task")
    description: str = Field(
        max_length=400,
        description="An explanation of what must be executed on this task, containing inputs, outputs and previous dependencies.",
    )
    signature_function: str = Field(
        description="Name of the python signature function that must be implemented by the task.",
    )
    data_source_id: UUID = Field(
        description="Data Source Schema that this task belongs to",
    )


class TaskSchema(TaskCreateSchema):
    id: UUID = Field(
        default_factory=uuid4, alias="id", description="Unique identifier for the task."
    )

    def __str__(self) -> str:
        return f"Title: {self.title}\nDescription: {self.description}\n"

    class Config(BaseSchema.Config):
        from_attributes = True
