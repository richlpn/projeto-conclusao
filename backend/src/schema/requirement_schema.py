from uuid import UUID, uuid4

from src.models.domain.requirement import Requirement
from src.models.domain.task import Task
from src.schema.task_schema import BaseSchema, Field, TaskSchema


class RequirementSchema(BaseSchema[Requirement]):
    id: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the requirement"
    )
    title: str = Field(description="Requirement title")
    tasks: list[BaseSchema[Task]] = Field(
        default_factory=list,
        description="List of task to be completed in order to fulfill this requirement.",
    )

    def to_model(self) -> Requirement:
        model = self.model_dump()
        model["tasks"] = [task.to_model() for task in self.tasks]
        return Requirement(model)

    @classmethod
    def from_model(cls, model: Requirement) -> BaseSchema[Requirement]:
        return cls(**model.__dict__)
