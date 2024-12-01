from uuid import UUID

from fastapi import Depends
from src.models.domain.data_source import DataSourceColumn
from src.repositories.data_source_columns_repository import DataSourceColumnRepository
from src.schema.data_source_column_schema import (
    DataSourceColumnCreateSchema,
    DataSourceColumnSchema,
    DataSourceColumnUpdateSchema,
)
from src.repositories.base_repository import BaseRepository
from src.service.base_service import BaseService


class DataSourceColumnService(
    BaseService[
        DataSourceColumn,
        DataSourceColumnCreateSchema,
        DataSourceColumnUpdateSchema,
        DataSourceColumnSchema,
        UUID,
    ]
):

    def __init__(
        self,
        repository: BaseRepository[DataSourceColumn, UUID],
    ):
        super().__init__(DataSourceColumn, DataSourceColumnSchema, repository)


def get_data_source_column_service(
    repo=Depends(DataSourceColumnRepository),
) -> DataSourceColumnService:
    return DataSourceColumnService(repo)
