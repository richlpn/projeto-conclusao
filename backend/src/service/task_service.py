from uuid import UUID

from fastapi import Depends
from src.models.domain.task import Task
from src.repositories.task_repository import get_task_repository
from src.schema.task_schema import TaskCreateSchema, TaskUpdateSchema
from src.utils.base_repository import BaseRepository
from src.utils.base_service import BaseService


class TaskService(BaseService[Task, TaskCreateSchema, TaskUpdateSchema, UUID]):

    def __init__(self, repository: BaseRepository[Task, UUID]):
        super().__init__(Task, repository)


def get_task_service(repository=Depends(get_task_repository)):
    return TaskService(repository)
