from uuid import UUID

from fastapi import Depends
from src.models.domain.data_source.data_source import DataSource
from src.models.domain.data_source.data_source_column import DataSourceColumn
from src.models.domain.data_source.data_source_type import DataSourceType
from src.repositories.data_source_repository import get_data_source_repository
from src.schema.data_source_column_schema import DataSourceColumnSchema
from src.schema.data_source_schema import (
    DataSourceCreateSchema,
    DataSourceSchema,
    DataSourceUpdateSchema,
)

from src.repositories.base_repository import BaseRepository
from src.schema.data_source_type_schema import (
    DataSourceTypeCreateSchema,
    DataSourceTypeSchema,
    DataSourceTypeUpdateSchema,
)
from src.service.base_service import BaseService
from src.service.data_source_type_service import get_data_source_type_service


class DataSourceService(
    BaseService[
        DataSource,
        DataSourceCreateSchema,
        DataSourceUpdateSchema,
        DataSourceSchema,
        UUID,
    ]
):

    def __init__(
        self,
        repository: BaseRepository[DataSource, UUID],
        type_service: BaseService[
            DataSourceType,
            DataSourceTypeCreateSchema,
            DataSourceTypeUpdateSchema,
            DataSourceTypeSchema,
            UUID,
        ],
        schema=DataSourceSchema,
    ):
        super().__init__(DataSource, schema, repository)
        self.type_service = type_service

    def create(self, obj: DataSourceCreateSchema) -> DataSourceSchema:

        # Gets the type from the database using the informed DataSourceTypeSchema ID
        ds_type = self.type_service.get_by_id(obj.type)

        # From the create schema takes the name and ignores the "type" id
        # Replaces the type by the DataSourceTypeSchema found to try to create an valid DataSource
        schema = self.schema(**obj.model_dump(exclude={"type"}), type=ds_type)

        # The DataSourceTypeSchema isn't a valid SQLAlchemy model it must be removed
        # The DataSourceSchema has no type_id attribute so it must be set on it's resulting dict
        schema_dict = schema.model_dump(exclude={"type"})
        schema_dict["type_id"] = schema.type.id
        db_obj = self.model(**schema_dict)

        # By this point 'db_obj' has no attribute type only type_id
        self.repository.create(db_obj)
        return schema


def get_data_source_service(
    repo=Depends(get_data_source_repository),
    dst_service=Depends(get_data_source_type_service),
):
    return DataSourceService(repo, dst_service)
