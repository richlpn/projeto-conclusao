from uuid import UUID
from src.models.domain.requirement import Requirement
from src.utils.base_repository import BaseRepository


class RequirementRepository(BaseRepository[Requirement, UUID]):

    model = Requirement
