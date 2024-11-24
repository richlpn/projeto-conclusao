from uuid import UUID, uuid4

from src.config.dependency_injection import component
from src.config.dependency_injection.autowired import autowired
from src.models.domain.data_source.data_source import DataSource
from src.models.dtos.data_source_dto import DataSourceDTO
from src.repositories.data_source_repository import DataSourceRepository
from src.schema.data_source_schema import DataSourceSchema
from src.service.data_source_column_service import DataSourceColumnService
from src.utils.base_schema import BaseSchema
from src.utils.base_service import BaseService


@component()
class DataSourceService(BaseService[DataSource, DataSourceDTO, UUID]):

    @autowired
    def __init__(
        self, repository: DataSourceRepository, service: DataSourceColumnService
    ):
        super().__init__(repository)
        self.column_service = service

    def create(self, dto: DataSourceDTO) -> DataSource:
        columns = []
        for col in dto.columns:
            columns.append(self.column_service.create(col))

        data_source = DataSource(
            id=uuid4(),
            name=dto.name,
            columns=columns,
            type=dto.type,
            separator=dto.separator,
        )

        return self.repository.create(data_source)

    def update(self, id: UUID, dto: DataSourceDTO) -> DataSourceSchema | None:

        data_source = self.repository.get_by_id(id)

        data_source.name = dto.name  # type: ignore
        data_source.type = dto.type  # type: ignore
        data_source.separator = dto.separator  # type: ignore
        return self.repository.update(data_source)

    def get_by_id(self, id: UUID) -> DataSourceSchema | None:
        return self.repository.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BaseSchema[DataSource]]:
        sources = list(
            map(DataSourceSchema.from_model, self.repository.get_all(skip, limit))
        )
        print("Sources", sources)
        return sources

    def delete(self, id: UUID) -> bool:
        return self.repository.delete(id)
