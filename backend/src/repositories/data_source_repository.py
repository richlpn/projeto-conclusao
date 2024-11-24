from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from src.config.dependency_injection.component import component
from src.utils.base_repository import BaseRepository
from src.models.domain.data_source import DataSource


@component()
class DataSourceRepository(BaseRepository[DataSource, UUID]):

    model = DataSource

    def get_by_type(self, db: Session, type: str) -> List[DataSource]:
        """Get all data sources of a specific type."""
        return db.query(self.model).filter(self.model.type == type).all()
