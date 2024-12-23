from uuid import UUID, uuid4

from src.schema.script_schema import Script
from src.schema.task_schema import BaseSchema, Field, TaskCreateSchema, TaskSchema


class RequirementCreateSchema(BaseSchema):
    title: str = Field(description="Requirement title")
    tasks: list[TaskCreateSchema] = Field(
        description="List of task to be completed in order to fulfill this requirement.",
    )


class RequirementUpdateSchema(BaseSchema):
    title: str


class RequirementSchema(RequirementCreateSchema):
    id: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the requirement"
    )
    tasks: list[TaskSchema] = Field(
        description="List of task to be completed in order to fulfill this requirement.",
    )

    code: Script = Field(description="Python script generated from the tasks")

    class Config(BaseSchema.Config):
        from_attributes = True
