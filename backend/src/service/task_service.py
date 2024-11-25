from typing import List
from uuid import UUID

from src.config.dependency_injection import autowired, component
from src.models.domain.task import Task
from src.models.dtos.taskDTO import TaskDTO
from src.schema.task_schema import TaskSchema
from src.utils.base_repository import BaseRepository
from src.utils.base_schema import BaseSchema
from src.utils.base_service import BaseService


@component()
class TaskService(BaseService[Task, TaskDTO, UUID]):

    @autowired
    def __init__(self, repository: BaseRepository[Task, UUID]):
        super().__init__(repository)

    def create(self, dto: TaskDTO) -> BaseSchema[Task]:

        task_schema = TaskSchema(
            title=dto.title,
            description=dto.description,
            signature_function=dto.singature_function,
        )
        self.repository.create(task_schema.to_model())
        return task_schema

    def update(self, id: UUID, dto: TaskDTO) -> BaseSchema[Task] | None:
        task_model = self.repository.get_by_id(id=id)
        if not task_model:
            return

        task: TaskSchema = TaskSchema.from_model(task_model)
        task.description = dto.description
        task.title = dto.title
        task.signature_function = dto.singature_function
        return self.repository.update(task.to_model())

    def delete(self, id: UUID) -> bool:
        return self.repository.delete(id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[BaseSchema[Task]]:
        return [TaskSchema.from_model(m) for m in self.repository.get_all(skip, limit)]
