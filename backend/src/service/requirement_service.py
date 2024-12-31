from uuid import uuid4

from fastapi import Depends
from src.exceptions.rule_exception import RuleException
from src.graph.agents.task_creation_agent import RequirementsCreationAgent
from src.models.domain.data_source.data_source import DataSource
from src.models.dtos.requirements_dto import Requirement
from src.repositories.base_repository import BaseRepository
from src.repositories.requirement_repository import (
    RequirementRepository,
    get_requirement_repository,
)
from src.schema.data_source_schema import (
    DataSourceCreateSchema,
    DataSourceSchema,
    DataSourceUpdateSchema,
)
from src.schema.requirement_schema import (
    UUID,
    RequirementCreateSchema,
    RequirementSchema,
    RequirementUpdateSchema,
)
from src.schema.task_schema import TaskSchema
from src.service.base_service import BaseService
from src.service.data_source_service import get_data_source_service
from src.service.task_service import (
    Task,
    TaskCreateSchema,
    TaskUpdateSchema,
    get_task_service,
)


class RequirementService(
    BaseService[
        Requirement,
        RequirementCreateSchema,
        RequirementUpdateSchema,
        RequirementSchema,
        UUID,
    ]
):

    repository: RequirementRepository

    def __init__(
        self,
        repository: BaseRepository[Requirement, UUID],
        task_service: BaseService[
            Task, TaskCreateSchema, TaskUpdateSchema, TaskSchema, UUID
        ],
        data_source_service: BaseService[
            DataSource,
            DataSourceCreateSchema,
            DataSourceUpdateSchema,
            DataSourceSchema,
            UUID,
        ],
    ):
        self.task_service = task_service
        self.data_source_service = data_source_service
        super().__init__(Requirement, RequirementSchema, repository)

    def data_source_has_requirements(self, data_source_id: UUID) -> bool:
        cond = bool(self.repository.filter_by_data_source_id(data_source_id))
        print("HAS REQUIREMENT", cond)
        return cond

    def create(self, obj: RequirementCreateSchema):
        # Data Source ID is valid?
        self.data_source_service.get_by_id(obj.data_source_id)

        if self.data_source_has_requirements(obj.data_source_id):
            raise RuleException(
                "Requirement Limit",
                "The informed Data Source already has a Requirement",
            )

        schema = RequirementSchema(**obj.model_dump())
        self.repository.create(self.model(**schema.model_dump()))
        return schema

    def gen_from_data_source(self, data_source_id: UUID) -> RequirementSchema:
        data_source = self.data_source_service.get_by_id(data_source_id)

        if self.data_source_has_requirements(data_source_id):
            raise RuleException(
                "Requirement Limit",
                "The informed Data Source already has a Requirement!",
            )

        requirement_id = uuid4()
        tasks_schema = RequirementsCreationAgent(id=requirement_id).invoke(
            SCHEMA=data_source
        )
        schema = RequirementSchema(data_source_id=data_source.id, id=requirement_id)
        self.repository.create(self.model(**schema.model_dump()))

        for task in tasks_schema.tasks:
            task.requirement_id = requirement_id
            schema.tasks.append(self.task_service.create(task))

        return schema


def get_requirement_service(
    repo=Depends(get_requirement_repository),
    task_service=Depends(get_task_service),
    ds_service=Depends(get_data_source_service),
):
    return RequirementService(repo, task_service, ds_service)
