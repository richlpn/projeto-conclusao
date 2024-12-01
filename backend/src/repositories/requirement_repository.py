from uuid import UUID
from src.models.domain.requirements.requirement import Requirement
from src.utils.base_repository import BaseRepository


class RequirementRepository(BaseRepository[Requirement, UUID]):

    model = Requirement


def get_requirement_repository():
    return RequirementRepository()
