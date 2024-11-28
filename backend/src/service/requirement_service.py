from fastapi import Depends
from src.models.dtos.requirements_dto import Requirement
from src.repositories.requirement_repository import get_requirement_repository
from src.schema.requirement_schema import (
    UUID,
    RequirementCreateSchema,
    RequirementUpdateSchema,
)
from src.service.task_service import (
    Task,
    TaskCreateSchema,
    TaskUpdateSchema,
    get_task_service,
)
from src.utils.base_repository import BaseRepository
from src.utils.base_service import BaseService


class RequirementService(
    BaseService[Requirement, RequirementCreateSchema, RequirementUpdateSchema, UUID]
):

    def __init__(
        self,
        repository: BaseRepository[Requirement, UUID],
        task_service: BaseService[Task, TaskCreateSchema, TaskUpdateSchema, UUID],
    ):
        self.task_service = task_service
        super().__init__(Requirement, repository)

    def create(self, obj: RequirementCreateSchema) -> Requirement:
        tasks = [self.task_service.create(task) for task in obj.tasks]
        obj_dict = obj.model_dump(exclude={"tasks"})
        obj_dict["tasks"] = tasks
        model = self.repository.create(self.model(**obj_dict))
        return model


def get_requirement_service(
    repo=Depends(get_requirement_repository), task_service=Depends(get_task_service)
):
    return RequirementService(repo, task_service)
