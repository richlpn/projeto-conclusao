from uuid import UUID

from src.config.dependency_injection.component import component
from src.models.domain.data_source import DataSourceColumn
from src.utils.base_repository import BaseRepository


@component()
class DataSourceColumnRepository(BaseRepository[DataSourceColumn, UUID]):

    model = DataSourceColumn

    