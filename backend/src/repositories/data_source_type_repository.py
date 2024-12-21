from typing import Type
from uuid import UUID
from src.models.domain.data_source.data_source_type import DataSourceType
from src.repositories.base_repository import BaseRepository


class DataSourceTypeRepository(BaseRepository[DataSourceType, UUID]):

    def __init__(self, model=DataSourceType):
        super().__init__(model)


def get_data_source_type_repository() -> BaseRepository[DataSourceType, UUID]:
    return DataSourceTypeRepository()
