from uuid import UUID, uuid4

from src.schema.task_schema import BaseSchema, Field, TaskCreateSchema, TaskSchema


class RequirementCreateSchema(BaseSchema):
    data_source_id: UUID = Field(
        description="Data source id that will be used to generate the requirement code",
    )


class RequirementCreateFromLLMSchema(BaseSchema):
    tasks: list[TaskCreateSchema] = Field(
        description="List of task to be completed in order to fulfill this requirement.",
    )


class RequirementUpdateSchema(RequirementCreateFromLLMSchema): ...


class RequirementSchema(RequirementCreateSchema):
    id: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the requirement"
    )
    tasks: list[TaskSchema] = Field(
        description="List of task to be completed in order to fulfill this requirement.",
        default_factory=list,
    )

    code: str | None = Field(
        description="Python script generated from the tasks", default=None
    )

    class Config(BaseSchema.Config):
        from_attributes = True
