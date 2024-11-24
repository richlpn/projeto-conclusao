from uuid import uuid4
from pydantic import Field
from sqlalchemy import UUID
from src.models.task import Task
from src.utils.base_schema import BaseSchema


class TaskSchema(BaseSchema[Task]):
    id: UUID = Field(
        default_factory=uuid4, alias="id", description="Unique identifier for the task."
    )
    title: str = Field(description="A short descriptive title about the task")
    description: str = Field(
        description="A Detailed explanation of what must be executed on this task, containing inputs, ouputs and previous dependecies."
    )
    signature_function: str = Field(
        description="Name of the python signature function that must be implemented by the task."
    )

    def __str__(self) -> str:
        return f"Title: {self.title}\nDescription: {self.description}\n"

    @classmethod
    def from_model(cls, model: Task):
        return cls(**model.__dict__)

    def to_model(self) -> Task:
        return Task(**self.model_dump())
