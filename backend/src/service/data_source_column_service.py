from typing import List, Optional
from uuid import UUID, uuid4

from src.config.dependency_injection import autowired, component
from src.models.domain.data_source import DataSourceColumn
from src.models.dtos.data_source_column_dto import DataSourceColumnDTO
from src.repositories.data_source_columns_repository import DataSourceColumnRepository
from src.schema.data_source_column_schema import DataSourceColumnSchema
from src.utils.base_schema import BaseSchema
from src.utils.base_service import BaseService


@component()
class DataSourceColumnService(BaseService[DataSourceColumn, DataSourceColumnDTO, UUID]):

    @autowired
    def __init__(self, repository: DataSourceColumnRepository):
        super().__init__(repository)

    def create(self, dto: DataSourceColumnDTO) -> DataSourceColumn:
        column = DataSourceColumn(
            id=uuid4(), name=dto.name, type=dto.type, description=dto.description
        )
        return self.repository.create(column)

    def get_by_id(self, id: UUID) -> Optional[DataSourceColumn]:
        return self.repository.get_by_id(id)

    def update(self, id: UUID, dto: DataSourceColumnDTO) -> Optional[DataSourceColumn]:
        column = DataSourceColumn(
            id=uuid4(), name=dto.name, type=dto.type, description=dto.description
        )
        return self.repository.update(column)

    def delete(self, id: UUID) -> bool:
        return self.repository.delete(id)

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> List[BaseSchema[DataSourceColumn]]:
        sources = list(
            map(DataSourceColumnSchema.from_model, self.repository.get_all(skip, limit))
        )
        return sources
