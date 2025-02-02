from uuid import UUID

from fastapi import Depends
from src.config.database import query
from src.models.data_source import DataSourceColumn
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
    repository: DataSourceColumnRepository

    def __init__(
        self,
        repository: BaseRepository[DataSourceColumn, UUID],
    ):
        super().__init__(DataSourceColumn, DataSourceColumnSchema, repository)

    @query
    def filter_by_dataSourceId(
        self, data_source_id: UUID
    ) -> list[DataSourceColumnSchema]:
        """
        Finds all DataSourceColumns associated with a given DataSource id.

        Args:
        - data_source_id (UUID): The id of the DataSource.

        Returns:
        - list[DataSourceColumnSchema]: A list of DataSourceColumnSchema objects.
        """
        ...


def get_data_source_column_service(
    repo=Depends(DataSourceColumnRepository),
) -> DataSourceColumnService:
    return DataSourceColumnService(repo)
