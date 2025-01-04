from uuid import UUID, uuid4

from fastapi import Depends
from src.graph.agents.task_creation_agent import TaskCreationAgent
from src.models.domain.data_source.data_source import DataSource
from src.models.domain.requirements.task import Task
from src.repositories.base_repository import BaseRepository
from src.repositories.task_repository import get_task_repository
from src.schema.data_source_schema import (
    DataSourceCreateSchema,
    DataSourceSchema,
    DataSourceUpdateSchema,
)
from src.schema.requirement_schema import RequirementSchema
from src.schema.task_schema import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from src.service.base_service import BaseService
from src.service.data_source_service import get_data_source_service


class TaskService(
    BaseService[Task, TaskCreateSchema, TaskUpdateSchema, TaskSchema, UUID]
):

    def __init__(
        self,
        repository: BaseRepository[Task, UUID],
        data_source_service: BaseService[
            DataSource,
            DataSourceCreateSchema,
            DataSourceUpdateSchema,
            DataSourceSchema,
            UUID,
        ],
    ):
        super().__init__(Task, TaskSchema, repository)
        self.data_source_service = data_source_service

    def gen_from_data_source(self, data_source_id: UUID) -> list[TaskSchema]:
        data_source = self.data_source_service.get_by_id(data_source_id)
        tasks_schema = TaskCreationAgent(id=data_source_id).invoke(SCHEMA=data_source)
        tasks = []
        for task in tasks_schema.tasks:
            tasks.append(self.create(task))

        return tasks


def get_task_service(
    repository=Depends(get_task_repository),
    data_source_service=Depends(get_data_source_service),
):
    return TaskService(repository, data_source_service)
