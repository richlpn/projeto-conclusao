from pydantic import Field
from sqlalchemy import UUID
from src.models.domain.requirement import Requirement
from src.models.dtos.taskDTO import TaskDTO
from src.utils.base_dto import BaseDTO


class RequirementDTO(BaseDTO[Requirement]):

    title: str = Field()
    tasks: list[TaskDTO] = Field(default_factory=list)
    data_source_id: UUID = Field()
