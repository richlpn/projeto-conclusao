from uuid import UUID
from src.models.domain.requirements.task import Task
from src.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task, UUID]):

    model = Task

    def __init__(self, model=Task):
        super().__init__(model)


def get_task_repository():
    return TaskRepository()
