from uuid import UUID
from src.models.domain.data_source.data_source_type import DataSourceType
from src.repositories.base_repository import BaseRepository


class DataSourceColumnRepository(BaseRepository[DataSourceType, UUID]):

    model = DataSourceType
