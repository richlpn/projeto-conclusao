from typing import List
from uuid import UUID
from fastapi import Depends
from src.models.domain.data_source.data_source_type import DataSourceType
from src.repositories.base_repository import BaseRepository
from src.repositories.data_source_type_repository import get_data_source_type_repository
from src.schema.data_source_type_schema import (
    DataSourceTypeCreateSchema,
    DataSourceTypeSchema,
    DataSourceTypeUpdateSchema,
)
from src.service.base_service import BaseService


class DataSourceTypeService(
    BaseService[
        DataSourceType,
        DataSourceTypeCreateSchema,
        DataSourceTypeUpdateSchema,
        DataSourceTypeSchema,
        UUID,
    ]
):

    def __init__(
        self,
        repository: BaseRepository[DataSourceType, UUID],
    ):
        super().__init__(DataSourceType, DataSourceTypeSchema, repository)

    def create(self, obj: DataSourceTypeCreateSchema) -> DataSourceTypeSchema:
        return super().create(obj)

    def update(self, id: UUID, obj: DataSourceTypeUpdateSchema) -> DataSourceTypeSchema:
        return super().update(id, obj)

    def delete(self, id: UUID):
        return super().delete(id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DataSourceTypeSchema]:
        return super().get_all(skip, limit)

    def get_by_id(self, id: UUID) -> DataSourceTypeSchema:
        return super().get_by_id(id)


def get_data_source_type_service(
    repo=Depends(get_data_source_type_repository),
) -> BaseService[
    DataSourceType,
    DataSourceTypeCreateSchema,
    DataSourceTypeUpdateSchema,
    DataSourceTypeSchema,
    UUID,
]:
    return DataSourceTypeService(repo)
