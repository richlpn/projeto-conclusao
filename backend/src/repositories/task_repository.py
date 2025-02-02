from uuid import UUID
from src.config.database import query
from src.models.task import Task
from src.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task, UUID]):

    model = Task

    def __init__(self, model=Task):
        super().__init__(model)

    @query
    def filter_by_dataSourceId(self, id: UUID) -> list[Task]: ...


def get_task_repository():
    return TaskRepository()
