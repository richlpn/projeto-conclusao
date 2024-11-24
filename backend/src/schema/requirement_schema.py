from uuid import UUID
from pydantic import BaseModel, Field
from src.schema.task_schema import TaskSchema


class RequirementSchema(BaseModel):
    id: UUID = Field(
        ..., alias="id", description="Unique identifier for the requirement"
    )
    title: str = Field(description="Requirement title")
    tasks: list[TaskSchema] = Field(
        default_factory=list,
        description="List of task to be completed in order to fulfill this requirement.",
    )
