from uuid import UUID
from src.models.domain.data_source.data_source_type import DataSourceType
from src.repositories.base_repository import BaseRepository


class DataSourceTypeRepository(BaseRepository[DataSourceType, UUID]):

    model = DataSourceType


def get_data_source_type_repository() -> BaseRepository[DataSourceType, UUID]:
    return DataSourceTypeRepository()
