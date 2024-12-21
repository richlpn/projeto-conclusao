from typing import Type
from uuid import UUID

from src.models.domain.data_source import DataSourceColumn
from src.repositories.base_repository import BaseRepository, query


class DataSourceColumnRepository(BaseRepository[DataSourceColumn, UUID]):

    def __init__(self):
        super().__init__(DataSourceColumn)

    @query
    def filter_by_data_source_id(
        self,
        data_source_id: UUID,
    ) -> list[DataSourceColumn]: ...
