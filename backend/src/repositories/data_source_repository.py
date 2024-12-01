from typing import List
from uuid import UUID

from src.models.domain.data_source import DataSource
from src.repositories.base_repository import BaseRepository


class DataSourceRepository(BaseRepository[DataSource, UUID]):

    model = DataSource

    def get_by_type(self, type: str) -> List[DataSource]:
        """Get all data sources of a specific type."""
        return self.db.query(self.model).filter(self.model.type == type).all()


def get_data_source_repository():
    return DataSourceRepository()
