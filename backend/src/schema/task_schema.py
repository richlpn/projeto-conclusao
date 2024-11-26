from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field
from src.models.domain.task import Task
from src.utils.base_schema import BaseSchema


class TaskUpdateSchema(BaseSchema[Task]):
    title: Optional[str]
    description: Optional[str] = Field(
        max_length=200,
    )
    signature_function: Optional[str] = Field(
        max_length=20,
    )


class TaskCreateSchema(BaseSchema[Task]):
    title: Optional[str] = Field(
        max_length=20, description="A short descriptive title about the task"
    )
    description: str = Field(
        max_length=200,
        description="A Detailed explanation of what must be executed on this task, containing inputs, outputs and previous dependencies.",
    )
    signature_function: str = Field(
        max_length=20,
        description="Name of the python signature function that must be implemented by the task.",
    )


class TaskSchema(TaskCreateSchema):
    id: UUID = Field(
        default_factory=uuid4, alias="id", description="Unique identifier for the task."
    )

    def __str__(self) -> str:
        return f"Title: {self.title}\nDescription: {self.description}\n"

    class Config(BaseSchema.Config):
        orm_mode = True
