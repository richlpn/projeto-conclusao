from uuid import UUID
from src.config.dependency_injection import component
from src.models.domain.task import Task
from src.utils.base_repository import BaseRepository


@component(BaseRepository[Task, UUID])
class TaskRepository(BaseRepository[Task, UUID]):

    model = Task
