from typing import Type
from uuid import UUID

from src.config.database import query
from src.models.data_source import DataSourceColumn
from src.repositories.base_repository import BaseRepository


class DataSourceColumnRepository(BaseRepository[DataSourceColumn, UUID]):

    def __init__(self):
        super().__init__(DataSourceColumn)

    @query
    def filter_by_dataSourceId(
        self,
        data_source_id: UUID,
    ) -> list[DataSourceColumn]: ...
