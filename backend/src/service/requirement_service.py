from typing import List

from src.config.dependency_injection import component, autowired
from src.models.domain.task import Task
from src.models.dtos.requirements_dto import RequirementDTO, Requirement
from src.models.dtos.taskDTO import TaskDTO
from src.schema.requirement_schema import UUID, RequirementSchema, BaseSchema
from src.utils.base_service import BaseService, BaseRepository


@component
class RequirementService(BaseService[Requirement, RequirementDTO, UUID]):

    @autowired
    def __init__(
        self,
        repository: BaseRepository[Requirement, UUID],
        task_service: BaseService[Task, TaskDTO, UUID],
    ):
        self.task_service = task_service
        super().__init__(repository)

    def create(self, dto: RequirementDTO) -> BaseSchema[Requirement]:
        tasks = list(map(self.task_service.create, dto.tasks))
        req = RequirementSchema(**dto.model_dump(), tasks=tasks)
        return self.repository.create(req.to_model())

    def get_all(self, skip: int = 0, limit: int = 100) -> List[BaseSchema[Requirement]]:
        req = self.repository.get_all(skip=skip, limit=limit)
        req = list(map(RequirementSchema.from_model, req))
        return req

    def get_by_id(self, id: UUID) -> BaseSchema[Requirement] | None:
        return self.repository.get_by_id(id)

    def update(self, id: UUID, dto: RequirementDTO) -> BaseSchema[Requirement] | None:
        old = self.repository.get_by_id(id)

        if not old:
            return
        old.__dict__.update(dto.model_dump())
        task = RequirementSchema(**old.__dict__)
        return self.repository.update(task.to_model())

    def delete(self, id: UUID) -> bool:
        return self.repository.delete(id)
