from uuid import UUID

from fastapi import Depends
from src.models.domain.data_source.data_source import DataSource
from src.models.domain.data_source.data_source_column import DataSourceColumn
from src.repositories.data_source_repository import DataSourceRepository

from src.schema.data_source_schema import DataSourceCreateSchema, DataSourceUpdateSchema
from src.service.data_source_column_service import (
    DataSourceColumnCreateSchema,
    DataSourceColumnService,
    DataSourceColumnUpdateSchema,
)
from src.utils.base_repository import BaseRepository
from src.utils.base_service import BaseService


class DataSourceService(
    BaseService[DataSource, DataSourceCreateSchema, DataSourceUpdateSchema, UUID]
):

    def __init__(
        self,
        repository: BaseRepository[DataSource, UUID],
        column_service: BaseService[
            DataSourceColumn,
            DataSourceColumnCreateSchema,
            DataSourceColumnUpdateSchema,
            UUID,
        ],
    ):
        self.column_service = column_service
        super().__init__(DataSource, repository)

    def create(self, obj: DataSourceCreateSchema) -> DataSource:
        columns = [self.column_service.create(col) for col in obj.columns]
        model = self.model(obj.model_dump().update({"columns": columns}))
        return self.repository.create(model)


def get_data_source_service(
    repo=Depends(DataSourceRepository), column_service=Depends(DataSourceColumnService)
):
    return DataSourceService(repo, column_service)
