from uuid import UUID
from src.models.domain.requirements.task import Task
from src.utils.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task, UUID]):

    model = Task


def get_task_repository():
    return TaskRepository()
