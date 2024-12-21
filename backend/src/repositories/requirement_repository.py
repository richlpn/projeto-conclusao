from typing import Type
from uuid import UUID
from src.models.domain.requirements.requirement import Requirement
from src.repositories.base_repository import BaseRepository


class RequirementRepository(BaseRepository[Requirement, UUID]):

    def __init__(self, model=Requirement):
        super().__init__(model)


def get_requirement_repository():
    return RequirementRepository()
