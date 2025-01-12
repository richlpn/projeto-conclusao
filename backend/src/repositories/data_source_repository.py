from uuid import UUID

from src.models.data_source import DataSource
from src.repositories.base_repository import BaseRepository


class DataSourceRepository(BaseRepository[DataSource, UUID]):

    model = DataSource

    def __init__(self, model=DataSource):
        super().__init__(model)


def get_data_source_repository():
    return DataSourceRepository()
