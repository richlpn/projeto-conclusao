from uuid import UUID

from src.models.domain.data_source import DataSourceColumn
from src.repositories.base_repository import BaseRepository


class DataSourceColumnRepository(BaseRepository[DataSourceColumn, UUID]):

    model = DataSourceColumn
