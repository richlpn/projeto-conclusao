from uuid import UUID
from src.models.domain.requirements.task import Task
from src.repositories.base_repository import BaseRepository, query


class TaskRepository(BaseRepository[Task, UUID]):

    model = Task

    def __init__(self, model=Task):
        super().__init__(model)

    @query
    def filter_by_data_source_id(self, id: UUID) -> list[Task]: ...


def get_task_repository():
    return TaskRepository()
