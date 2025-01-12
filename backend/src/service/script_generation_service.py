from uuid import UUID
from fastapi import Depends
from src.graph.agents.script_generator_agent import ScriptGeneratorAgent
from src.graph.nodes.script_generation_node import generate_python_script

from src.schema.data_source_schema import DataSourceUpdateSchema
from src.schema.task_schema import TaskCreateSchema
from src.service.crud_service import CrudService
from src.service.data_source_service import DataSourceService, get_data_source_service
from src.service.task_service import TaskService, get_task_service


class ScriptGenerationService(CrudService[str]):

    def __init__(
        self, task_service: TaskService, data_source_service: DataSourceService
    ):
        self.task_service = task_service
        self.data_source_service = data_source_service

    def create(self, data_source_id: UUID) -> str:
        tasks = self.task_service.get_from_data_source(data_source_id)
        tasks = [TaskCreateSchema.model_validate(task) for task in tasks]
        script = generate_python_script(ScriptGeneratorAgent(), tasks)
        self.data_source_service.update(
            data_source_id, DataSourceUpdateSchema(script=script)
        )
        return script

    def update(self, *arg, **kwargs) -> str: ...

    def delete(self, *args, **kwargs): ...

    def get_by_id(self, *args, **kwargs) -> str: ...

    def get_all(self, *args, **kwargs) -> list[str]:
        raise NotImplementedError()


def get_script_generation_service(
    task_service=Depends(get_task_service),
    data_source_service=Depends(get_data_source_service),
):
    return ScriptGenerationService(task_service, data_source_service)
