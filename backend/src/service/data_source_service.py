from uuid import UUID

from fastapi import Depends, UploadFile
from pydantic import ValidationError
from src.graph.tools.extract_docs_schema_tool import extract_schema_columns
from src.models.data_source.data_source import DataSource
from src.models.data_source.data_source_column import DataSourceColumn
from src.models.data_source.data_source_type import DataSourceType
from src.repositories.base_repository import BaseRepository
from src.repositories.data_source_repository import get_data_source_repository
from src.schema.data_source_column_schema import (
    DataSourceColumnCreateSchema,
    DataSourceColumnSchema,
    DataSourceColumnUpdateSchema,
)
from src.schema.data_source_schema import (
    DataSourceCreateSchema,
    DataSourceSchema,
    DataSourceUpdateSchema,
)
from src.schema.data_source_type_schema import (
    DataSourceTypeCreateSchema,
    DataSourceTypeSchema,
    DataSourceTypeUpdateSchema,
)
from src.service.base_service import BaseService
from src.service.data_source_column_service import get_data_source_column_service
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
        column_service: BaseService[
            DataSourceColumn,
            DataSourceColumnCreateSchema,
            DataSourceColumnUpdateSchema,
            DataSourceColumnSchema,
            UUID,
        ],
        schema=DataSourceSchema,
    ):
        super().__init__(DataSource, schema, repository)
        self.type_service = type_service
        self.column_service = column_service

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
        db_model = self.model(**schema_dict)
        self.repository.create(db_model)

        # From this point the database object has no attribute type only type_id
        return schema

    def from_file_text(self, file: UploadFile) -> DataSourceSchema:
        """Takes an file and uses an LLM to extract the Data Source data"""
        content = file.file.read().decode(errors="replace")
        schema, columns = extract_schema_columns(
            content=content, data_source_types=self.type_service.get_all()
        )
        created_schema = self.create(schema)

        for column in columns:
            col_dict = column.model_dump()
            col_dict["data_source_id"] = created_schema.id
            try:
                valid_col = DataSourceColumnCreateSchema.model_validate(col_dict)
                self.column_service.create(valid_col)
            except ValidationError:
                pass

        return created_schema


def get_data_source_service(
    repo=Depends(get_data_source_repository),
    dst_service=Depends(get_data_source_type_service),
    column_service=Depends(get_data_source_column_service),
):
    return DataSourceService(repo, dst_service, column_service)
