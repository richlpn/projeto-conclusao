from uuid import UUID
from src.config.dependency_injection.component import component
from src.models.domain.requirement import Requirement
from src.utils.base_repository import BaseRepository


@component(BaseRepository[Requirement, UUID])
class RequirementRepository(BaseRepository[Requirement, UUID]):

    model = Requirement
