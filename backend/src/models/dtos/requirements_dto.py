from uuid import UUID
from pydantic import Field
from src.models.domain.requirements.requirement import Requirement
from src.models.dtos.taskDTO import TaskDTO
from src.models.dtos.base_dto import BaseDTO


class RequirementDTO(BaseDTO[Requirement]):

    title: str = Field()
    tasks: list[TaskDTO] = Field(default_factory=list)
    data_source_id: UUID = Field()
