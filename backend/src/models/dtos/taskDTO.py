from src.models.domain.task import Task
from src.utils.base_dto import BaseDTO


class TaskDTO(BaseDTO[Task]):

    title: str
    description: str
    singature_function: str
