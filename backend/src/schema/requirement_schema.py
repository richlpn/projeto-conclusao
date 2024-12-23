from uuid import UUID, uuid4

from src.schema.task_schema import BaseSchema, Field, TaskCreateSchema, TaskSchema


class _ReqCreateSchema(BaseSchema):
    title: str = Field(description="Requirement title")

    data_source_id: UUID = Field(
        description="Data source id that will be used to generate the requirement code",
    )


class RequirementCreateSchema(_ReqCreateSchema):
    tasks: list[TaskCreateSchema] = Field(
        description="List of task to be completed in order to fulfill this requirement.",
    )


class RequirementUpdateSchema(BaseSchema):
    title: str


class RequirementSchema(_ReqCreateSchema):
    id: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the requirement"
    )
    tasks: list[TaskSchema] = Field(
        description="List of task to be completed in order to fulfill this requirement.",
    )

    code: str | None = Field(description="Python script generated from the tasks")

    class Config(BaseSchema.Config):
        from_attributes = True
