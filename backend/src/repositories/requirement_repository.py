from uuid import UUID
from src.models.domain.requirements.requirement import Requirement
from src.repositories.base_repository import BaseRepository, query


class RequirementRepository(BaseRepository[Requirement, UUID]):

    def __init__(self, model=Requirement):
        super().__init__(model)

    @query
    def filter_by_data_source_id(self, id: UUID) -> Requirement: ...


def get_requirement_repository():
    return RequirementRepository()
