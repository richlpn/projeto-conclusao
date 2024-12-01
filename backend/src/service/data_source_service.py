from uuid import UUID

from fastapi import Depends
from src.models.domain.data_source.data_source import DataSource
from src.models.domain.data_source.data_source_column import DataSourceColumn
from src.repositories.data_source_repository import get_data_source_repository
from src.schema.data_source_column_schema import DataSourceColumnSchema
from src.schema.data_source_schema import (
    DataSourceCreateSchema,
    DataSourceSchema,
    DataSourceUpdateSchema,
)
from src.service.data_source_column_service import (
    DataSourceColumnCreateSchema,
    DataSourceColumnUpdateSchema,
    get_data_source_column_service,
)
from src.repositories.base_repository import BaseRepository
from src.service.base_service import BaseService


class DataSourceService(
    BaseService[
        DataSource,
        DataSourceCreateSchema,
        DataSourceUpdateSchema,
        DataSourceSchema,
        UUID,
    ]
):

    def __init__(
        self,
        repository: BaseRepository[DataSource, UUID],
        schema=DataSourceSchema,
    ):
        super().__init__(DataSource, schema, repository)

    def create(self, obj: DataSourceCreateSchema) -> DataSourceSchema:
        model = self.model(**obj.model_dump())
        self.repository.create(model)
        return model


def get_data_source_service(
    repo=Depends(get_data_source_repository),
):
    return DataSourceService(repo)
